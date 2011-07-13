from pylabs import q, p

import os
import urllib
import inspect
import re
import functools

ADMINSPACE = "Admin"
IMPORTSPACE = "Imported"

class Alkira:
    def __init__(self, api=None):
        """
        Initialize the alkira library with a certain API
        
        @param api: The application api (in APPSERVER content)
        """
        self.KNOWN_TYPES = ["py", "md", "html", "txt"]
        
        self.connection = api.model.ui
        self.api = api

    def _getPageInfo(self, space, name):
        page_filter = self.connection.page.getFilterObject()
        page_filter.add('ui_view_page_list', 'name', name, True)
        page_filter.add('ui_view_page_list', 'space', space, True)
        page_info = self.connection.page.findAsView(page_filter, 'ui_view_page_list')
        return page_info

    def _getSpaceGuid(self, space):
        if isinstance(space, basestring):
            if q.basetype.guid.check(space):
                return space
            else:
                spaces = self._getSpaceInfo(space)
                if not spaces:
                    q.errorconditionhandler.raiseError("Space %s does not exist." % space)
                return spaces[0]['guid']
        elif isinstance(space, self.connection.space._ROOTOBJECTTYPE):
            return space.guid

    def _getSpaceInfo(self, name=None):
        filter = self.connection.space.getFilterObject()
        if name:
            filter.add('ui_view_space_list', 'name', name, True)
        space = self.connection.space.findAsView(filter, 'ui_view_space_list')
        return space

    def _getUserInfo(self, name=None):
        filter = self.connection.user.getFilterObject()
        if name:
            filter.add('ui_view_user_list', 'name', name, True)
        user = self.connection.user.findAsView(filter, 'ui_view_user_list')
        return user

    def _getParentGUIDS(self, guid_list):
        parent_list = []
        for guid in guid_list:
            page = self.connection.page.get(guid)
            if page.parent:
                parent_list.append(page.parent)

        return parent_list

    def _getDir(self, space, page=None):
        fullName = space
        if page:
            fullName = q.system.fs.joinPaths(space, page)
            
        return q.system.fs.joinPaths(q.dirs.pyAppsDir, self.api.appname, 'portal', 'spaces', fullName)

    def _getType(self, pagename):
        idx = pagename.rfind(".")
        if idx <= 0:
            return None
        ext = pagename[idx + 1:]
        if ext not in self.KNOWN_TYPES:
            return None
        return ext

    #rename doesn't work accross different mount points but has higher performance, so we implemented this move functions
    def _moveFile(self, filePath, new_name):
        try:
            q.system.fs.renameFile(filePath, new_name)
        except:
            q.system.fs.moveFile(filePath, new_name)

    def _moveDir(self, filePath, new_name):
        try:
            q.system.fs.renameDir(filePath, new_name)
        except:
            q.system.fs.moveDir(filePath, new_name)
            
    def _syncImportedPageToFile(self, spacename, page, action, oldname = None):
        """
        @param page: its the page object for action "delete" it can be the page's name instead
        @param action: "create", "update", "delete", "rename"
        @param newname: if action is "rename", newname is the new page's name/path
        Please note that "rename" action ALSO saves the file's content in the new location
        """
        if isinstance(page, str):
            if action != "delete":
                raise ValueError("Page object required for action %s"%action)
            pagename = page
        else:
            pagename = page.name

        #This function only save pages if its name contain its relative path

        if pagename.find("/") < 1:
            if action == "rename":
                raise ValueError("Invalid name for an imported page %s, name should be projectname/path/to/file.ext"%pagename)
            else:
                return False
        #get space path
        path = q.system.fs.joinPaths(q.dirs.pyAppsDir , self.api.appname, "portal", "spaces", spacename)
        filename = q.system.fs.joinPaths(path, pagename)
        if action in ("create", "update"):
            q.system.fs.writeFile(filename, page.content or "")
        elif action == "delete":
            if q.system.fs.exists(filename):
                q.system.fs.removeFile(filename)
        elif action == "rename":
            oldfilename = q.system.fs.joinPaths(path, oldname)
            #delete the old file
            if q.system.fs.exists(oldfilename):
                q.system.fs.removeFile(oldfilename)
            #save the new file
            q.system.fs.writeFile(filename, page.content or "")

    def listPages(self, space=None):
        """
        Lists all the pages in a certain space.

        @param space: The name, guid or space object of the space.
        """
        return map(lambda i: i['name'],
                   self.listPageInfo(space))

    def countPages(self, space=None):
        where = ''
        if space:
            space = self._getSpaceGuid(space)
            where = "where space='%s'" % space
            
        return self.connection.page.query("SELECT count(guid) from ui_page.ui_view_page_list %s;" % where)[0]['count']
    
    def search(self, text=None, space=None, category=None, tags=None):
        # ignore tags for now

        if not any([text, space, category, tags]):
            return []

        sql_select = 'page.category, page."name", space.name as space'
        sql_from = 'ui_page.ui_view_page_list as page join ui_space.ui_view_space_list as space on page.space = space.guid'
        sql_where = ['1=1']

        if tags:
            # MNour - A hackish solution for tags/labels search. @see PYLABS-14.
            # MNOUR - IMO this should be solved in the REST layer.
            tags = urllib.unquote_plus(tags)
            tags = tags.strip(', ')
            sql_where.append('page.tags LIKE \'%%%s%%\'' %  tags)

        if space:
            space = self.alkira.getSpace(space)
            sql_where.append('page.space = \'%s\'' % space.guid)

        if category:
            sql_where.append('page.category = \'%s\'' % category)

        if text:
            sql_where.append('page.content LIKE \'%%%s%%\'' % text)

        query = 'SELECT %s FROM %s WHERE %s' % (sql_select, sql_from, ' AND '.join(sql_where))

        result = self.connection.page.query(query)

        return result
    
    def listSpaces(self):
        """
        Lists all the spaces.
        """
        return map(lambda item: item["name"],
                   self.listSpaceInfo())

    def listSpaceInfo(self, name=None):
        """
        List all spaces info
        """
        spaces = self._getSpaceInfo(name)

        def byOrder(x, y):
            #Always put the admin space last
            if x["name"] == ADMINSPACE:
                return 1
            elif y["name"] == ADMINSPACE:
                return -1

            if "order" in x and x["order"] != None:
                if "order" in y and y["order"] != None:
                    return cmp(x["order"], y["order"])
                else:
                    return -1
            else:
                if "order" in y and y["order"] != None:
                    return 1
                else:
                    return 0

        spaces.sort(byOrder)
        return spaces

    def listPageInfo(self, space=None):
        """
        Lists all the pages in a space with their info.

        @param space: The name, guid or space object of the space.
        """
        filter = self.connection.page.getFilterObject()
        if space:
            space = self._getSpaceGuid(space)
            filter.add('ui_view_page_list', 'space', space, True)

        return self.connection.page.findAsView(filter, 'ui_view_page_list')

    def listUsers(self, name=None):
        return map(lambda item: item["name"],
                   self.listUserInfo(name))

    def listUserInfo(self, name=None):
        """
        Lists all the users

        @param space: The name of the user.
        """
        return self._getUserInfo(name)

    def listChildPages(self, space, name = None):
        """
        Lists child pages of page "name"

        @type space: String
        @param space: The name of the space.

        @type name: String
        @param name: The name of the parent page.
        """
        space = self._getSpaceGuid(space)
        filter = self.connection.page.getFilterObject()
        filter.add('ui_view_page_list', 'space', space, True)
        #Get page guid
        if name:
            guid = self._getPageInfo(space, name)[0]["guid"]
            filter.add('ui_view_page_list', 'parent', guid, True)
        else:
            filter.add('ui_view_page_list', 'parent', None, True)

        query = self.connection.page.findAsView(filter, 'ui_view_page_list')
        return list(name["name"] for name in query)

    def spaceExists(self, name):
        """
        Checks whether a space exists or not

        @param name: Space name

        @return: True if the space exists, False otherwise
        """
        return bool(self._getSpaceInfo(name))

    def pageExists(self, space, name):
        """
        Checks whether a page exists or not.

        @type space: String
        @param space: The name of the space.

        @type name: String
        @param name: The name of the page.

        @return: True if the page exists, False otherwise.
        """
        space = self._getSpaceGuid(space)
        if self._getPageInfo(space, name):
            return True
        else:
            return False

    def userExists(self, name):
        """
        Checks whether a user exists or not.

        @type name: String
        @param name: The name of the user

        @return: True if the user exists, False otherwise.
        """
        return bool(self._getUserInfo(name))

    def pageFind(self, name='', space='', category='', parent='', tags='', order=None, title='', exact_properties=None):
        filterObject = self.connection.page.getFilterObject()
        exact_properties = exact_properties or ()

        space = self._getSpaceGuid(space) if space else ''

        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)

        properties = ('name', 'space', 'category', 'parent', 'tags', 'order', 'title')
        for property_name, value in values.iteritems():
            if property_name in properties and not value in (None, ''):
                exact = property_name in exact_properties
                filterObject.add('ui_view_page_list', property_name, value, exactMatch=exact)

        return self.connection.page.find(filterObject)

    def userFind(self, name='', tags='', exact_properties=None):
        filterObject = self.connection.user.getFilterObject()
        exact_properties = exact_properties or ()

        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)

        properties = ('name', 'tags')
        for property_name, value in values.iteritems():
            if property_name in properties and not value in (None, ''):
                exact = property_name in exact_properties
                filterObject.add('ui_view_page_list', property_name, value, exactMatch=exact)

        return self.connection.user.find(filterObject)

    def getSpace(self, space):
        """
        Gets a space object

        @param name: The space name, or guid
        """
        if isinstance(space, self.connection.space._ROOTOBJECTTYPE):
            return space
        
        space = self._getSpaceGuid(space)
        return self.connection.space.get(space)

    def getPage(self, space, name):
        """
        Gets a page object.

        @type space: String
        @param space: The name of the space.

        @type name: String
        @param name: The name of the page.

        @return: Page object.
        """
        space = self._getSpaceGuid(space)
        page_info = self._getPageInfo(space, name)
        if not page_info:
            q.errorconditionhandler.raiseError("Page %s does not exist." % name)
        return self.connection.page.get(page_info[0]['guid'])

    def getUser(self, name):
        """
        Gets a user object.

        @type name: String
        @param name: The name of the user.

        @return: User object.
        """
        user_info = self._getUserInfo(name)
        if not user_info:
            q.errorconditionhandler.raiseError("User %s does not exist." % name)
        return self.connection.user.get(user_info[0]['guid'])

    def getPageByGUID(self, guid):
        """
        Get a page object by guid

        @param guid: Page guid
        """

        return self.connection.page.get(guid)

    def deleteSpace(self, space):
        """
        Delete space

        @param space: The space name, object or guid to delete

        @note: Deleting a space will delete all the pages in that space.
        """
        if space in (ADMINSPACE, IMPORTSPACE):
            raise ValueError("%s space is not deletable" % space)

        space = self.getSpace(space)

        pages = self.listPageInfo(space)

        for page in pages:
            if space == IMPORTSPACE:
                self._syncImportedPageToFile(space, page['name'], "delete")
            self.connection.page.delete(page['guid'])

        self.connection.space.delete(space.guid)
        self.deletePage(ADMINSPACE, space.name)
        q.system.fs.removeDirTree(self._getDir(space.name))

    def _syncPageToDisk(self, space, page, oldpagename=None):
        if space == IMPORTSPACE and page.name.find("/") > 0:
            return
        crumbs = self._breadcrumbs(page)
        _join = q.system.fs.joinPaths
        _isfile = q.system.fs.isFile
        _isdir = q.system.fs.isDir
        _write = q.system.fs.writeFile

        dir = self._getDir(space)
        upper = dir
        for i, level in enumerate(crumbs):
            name = level['name']
            filename = name + ".md"
            file = _join(dir, filename)
            dir = _join(dir, name)

            if i == len(crumbs) - 1:
                if oldpagename:
                    oldfile = _join(upper, oldpagename + ".md")
                    olddir = _join(upper, oldpagename)
                    tofile = file
                    if _isdir(olddir):
                        oldfile = _join(olddir, oldpagename)
                        tofile = _join(olddir, filename)

                    if _isfile(oldfile):
                        self._moveFile(oldfile, tofile)
                    if _isdir(olddir):
                        self._moveDir(olddir, dir)

                if _isdir(dir):
                    file = _join(dir, filename)
                _write(file, page.content)
            else:
                #in the chain
                if _isfile(file):
                    tmp = os.tmpnam()
                    self._moveFile(file, tmp)
                    q.system.fs.createDir(dir)
                    self._moveFile(tmp, _join(dir, filename))

            upper = dir

    def _syncPageDelete(self, space, crumbs):
        if space == IMPORTSPACE and page.name.find("/") > 0:
            return
        _join = q.system.fs.joinPaths
        _isfile = q.system.fs.isFile
        _isdir = q.system.fs.isDir

        dir = self._getDir(space)
        for i, level in enumerate(crumbs):
            name = level['name']
            filename = name + ".md"
            file = _join(dir, filename)
            dir = _join(dir, name)
            if i == len(crumbs) - 1:
                if _isdir(dir):
                    q.system.fs.removeDirTree(dir)
                elif _isfile(file):
                    q.system.fs.removeFile(file)
                    

    def deleteUser(self, name):
        """
        Deletes a user.

        @type name: String
        @param name: The name of the user.
        """
        user = self.getUser(name)
        self.connection.user.delete(user.guid)

    def deleteUserByGUID(self, userguid):
        """
        Deletes a user using its GUID

        @type userguid: GUID
        @param userguid: The GUID of the user.
        """
        self.connection.user.delete(userguid)

    def deletePageByGUID(self, guid):
        """
        Delete a page by guid

        @param guid: page guid
        """
        raise NotImplemented()
        self.connection.page.delete(guid)

    def deletePage(self, space, name):
        """
        Deletes a page and its chlidren (recursively).

        @type space: String
        @param space: The name of the space.

        @type name: String
        @param name: The name of the page.
        """
        
        def deleterecursive(guid):
            filter = self.connection.page.getFilterObject()
            filter.add("ui_view_page_list", "parent", guid, True)
            
            for chguid in self.connection.page.find(filter):
                deleterecursive(chguid)
            
            self.connection.page.delete(guid)
        
        page = self.getPage(space, name)
        crumbs = self._breadcrumbs(page)
        
        deleterecursive(page.guid)
        if space == IMPORTSPACE:
            self._syncImportedPageToFile(space, name, "delete")
        self._syncPageDelete(space, crumbs)

    def createSpace(self, name, tagsList=[], repository="", repo_username="", repo_password="", order=None):
        if self.spaceExists(name):
            q.errorconditionhandler.raiseError("Space %s already exists." % name)

        space = self.connection.space.new()
        space.name = name
        space.tags = ' '.join(tagsList)

        repo = space.repository.new()
        repo.url = repository
        repo.username = repo_username
        repo.password = repo_password
        space.repository = repo

        if not order:
            space.order = 10000
        else:
            space.order = order

        self.connection.space.save(space)

        if name == ADMINSPACE:
            return

        q.system.fs.createDir(self._getDir(name))

        #create a space page under the default admin space
        spacectnt = p.core.codemanagement.api.getSpacePage(name)
        self.createPage(name, "Home", content="", order=10000, title="Home", tagsList=tagsList)
        self.createPage(ADMINSPACE, name, spacectnt, title=name, parent="Spaces")
        
        return space
    
    def _breadcrumbs(self, page):
        breadcrumbs = []
        parent = page
        while parent:
            breadcrumbs.append({'guid': parent.guid,
                                'name': parent.name,
                                'title': parent.title})
            parent = self.getPageByGUID(parent.parent) if parent.parent else None

        breadcrumbs.reverse()
        return breadcrumbs

    def breadcrumbs(self, space, name):
        return self._breadcrumbs(self.alkira.getPage(space, name))
    
    def _createPage(self, space, name, content, order=None, title=None, tagsList=[], category='portal',
                   parent=None, filename=None, contentIsFilePath=False, pagetype="md"):
        
        space = self.getSpace(space)
        if self.pageExists(space.guid, name):
            q.errorconditionhandler.raiseError("Page %s already exists."%name)
        
        page = self.connection.page.new()
        params = {"name":name, "pagetype": pagetype, "space":space.guid, "category":category,
                  "title": title, "order": order, "filename":filename,
                  "content":q.system.fs.fileGetContents(content) if contentIsFilePath else content
                 }
        for key in params:
            if params[key] != None:
                setattr(page, key, params[key])

        if not order:
            page.order = 10000

        tags = set(tagsList)
        tags.add('space:%s' % space.name)
        tags.add('page:%s' % name)
        page.tags = ' '.join(tags)

        if parent:
            parent_page = self.getPage(space.guid, parent)
            page.parent = parent_page.guid

        self.connection.page.save(page)
        
        return page
    
    def createPage(self, space, name, content, order=None, title=None, tagsList=[], category='portal',
                   parent=None, filename=None, contentIsFilePath=False, pagetype="md"):
        """
        Creates a new page.

        @type space: String
        @param space: The name of the space.

        @type name: String
        @param name: The name of the page.

        @type content: String
        @param content: The content of the page. This can also be a file path; in this case you should set contentIsFilePath=True.

        @type order: Integer
        @param order: Order of the page

        @type title: String
        @param title: Title of the page

        @type tagsList: List
        @param tagsList: A list containing all the tags you want to add to the page.

        @type category: String
        @param category: The category of the page. Default is 'portal'.

        @type parent: String
        @param parent: If you want this to become a child page, add the name of the parent page to this parameter. Default is None.

        @type contentIsFilePath: Boolean
        @param contentIsFilePath: If the content you gave is a file path, set this value to True. Default is False.

        @type filename: string
        @param filename: used by import directory script to store original file path
        """
        space = self.getSpace(space)
        page = self._createPage(space=space, name=name, content=content,
                         order=order, title=title, tagsList=tagsList, category=category,
                         parent=parent, filename=filename, contentIsFilePath=contentIsFilePath,
                         pagetype=pagetype)
        
        if space.name == IMPORTSPACE:
            #the "Imported" space needs to keep filesystem in sync with database
            self._syncImportedPageToFile(space.name, page, "create")
        else:
            self._syncPageToDisk(space.name, page)
            
    def createUser(self, name, password, spaces=[], pages=[], tagsList=[]):
        """
        Create a new user object.

        @param name:             name of the user
        @type name:              string

        @param spaces:            list of user spaces
        @type spaces:             List

        @param pages:            list of user pages
        @type pages:             List

        @param tagsList:         tags of the page
        @type tags:              List
        """
        if self.userExists(name):
            q.errorconditionhandler.raiseError("User %s already exists."%name)
        else:
            user = self.connection.user.new()
            params = {"name":name, "password": password, "spaces":spaces, "pages":pages}
            for key in params:
                if params[key]:
                    setattr(user, key, params[key])

            tags = set(tagsList)
            tags.add('name:%s' % name)
            user.tags = ' '.join(tags)
            self.connection.user.save(user)
            return user

    def updateSpace(self, space, newname=None, tagslist=None, repository=None, repo_username=None, repo_password=None, order=None):
        space = self.getSpace(space)

        if space.name == ADMINSPACE:
            raise ValueError("Invalid space")
        oldname = space.name

        if newname != None and newname != oldname:
            if self.spaceExists(newname):
                q.errorconditionhandler.raiseError("Space %s already exists." % newname)
            space.name = newname

        if tagslist:
            space.tags = ' '.join(tagslist)

        if repository:
            space.repository.url = repository

        if repo_username:
            space.repository.username = repo_username

        if repo_password:
            space.repository.password = repo_password

        if order:
            space.order = order

        self.connection.space.save(space)

        if newname != None and oldname != newname:
            #rename space page.
            self.updatePage(ADMINSPACE, oldname, name=newname, content=p.core.codemanagement.api.getSpacePage(newname))
            
            #sync file system
            self._moveDir(self._getDir(oldname),
                          self._getDir(newname))
        
        return space

    def _updatePage(self, space, old_name, name=None, tagsList=None, content=None,
                   order=None, title=None, parent=None, category=None, pagetype=None, filename=None, contentIsFilePath=False):
        
        space = self.getSpace(space)
        spacename = space.name
        page = self.getPage(space.guid, old_name)
        
        type = None

        params = {"name": name, "pagetype": pagetype, "category":category,
                  "title": title, "order": order, "filename":filename,
                  "content":q.system.fs.fileGetContents(content) if contentIsFilePath else content
                  }

        for key in params:
            if params[key] != None:
                setattr(page, key, params[key])

        if tagsList:
            tags = set(page.tags.split(' '))
            for tag in tagsList:
                if tag not in tags:
                    tags.add(tag)

            page_tags = ' '.join(tags)
            page.tags = page_tags

        if parent:
            parent_page = self.getPage(space, parent)
            page.parent = parent_page.guid
        
        self.connection.page.save(page)
        
        return page
    
    def updatePage(self, space, old_name, name=None, tagsList=None, content=None,
                   order=None, title=None, parent=None, category=None, pagetype=None, filename=None, contentIsFilePath=False):
        """
        Updates an existing page.

        @type space: String
        @param space: The name of the space.

        @type old_name: String
        @param old_name: The name of the page.

        @type space: String
        @param space: Gives the page a new space.

        @type name: String
        @param name: Gives the page a new name.

        @type tagsList: List
        @param tagsList: Appends tags in this list to the current tags of the page.

        @type content: String
        @param content: The new content of the page. This can also be a file path; in this case you should set contentIsFilePath=True.

        @type order: Integer
        @param order: Order of the page

        @type title: String
        @param title: Title of the page

        @type category: String
        @param category: Gives the page a new category.

        @type parent: String
        @param parent: Gives the page a new parent.

        @type contentIsFilePath: Boolean
        @param contentIsFilePath: If the content you gave is a file path, set this value to True. Default is False.

        @type filename: string
        @param filename: used by import directory script to store original file path
        """
        
        space = self.getSpace(space)
        page = self._updatePage(space=space, old_name=old_name, name=name, tagsList=tagsList, content=content,
                         order=order, title=title, parent=parent, category=category,
                         pagetype=pagetype, filename=filename, contentIsFilePath=contentIsFilePath)
        
        if space.name == IMPORTSPACE:
            #the "Imported" space needs to keep filesystem in sync with database
            if name and name != old_name:
                self._syncImportedPageToFile(spacename, page, "rename", oldname = old_name)
            else:
                self._syncImportedPageToFile(spacename, page, "update")
        else:
            self._syncPageToDisk(space.name, page, old_name)
            
        return page

    def updateUser(self, old_user, name="", password="", tagsList=None):
        """
        Updates an existing page.

        @type old_user: String
        @param old_user: The name of the user.

        @type name: String
        @param name: Gives the user a new name.

        @type tagsList: List
        @param tagsList: Appends tags in this list to the current tags of the page.
        """

        user = self.getUser(old_user)
        if name:
            user.name = name
        if password:
            user.password = password

        if tagsList:
            tags = user.tags.split(' ')
            for tag in tagsList:
                tags.append(tag)

            user_tags = ' '.join(tags)
            user.tags = user_tags

        self.connection.user.save(user)
        return user


    def findMacroConfig(self, space="", page="", macro="", configId=None, username=None, exact_properties=None):
        configFilter = self.connection.config.getFilterObject()
        exact_properties = exact_properties or ()
        if space:
            space = self._getSpaceGuid(space)
            configFilter.add('ui_view_config_list', 'space', space, 'space' in exact_properties)
            if page:
                configFilter.add('ui_view_config_list', 'page', self._getPageInfo(space, page)[0]['guid'],
                    'page' in exact_properties)
        configFilter.add('ui_view_config_list', 'macro', macro, 'macro' in exact_properties)
        configFilter.add('ui_view_config_list', 'username', username, 'username' in exact_properties)
        if configId:
            configFilter.add('ui_view_config_list', 'configid', configId, 'configid' in exact_properties)
        return self.connection.config.findAsView(configFilter, 'ui_view_config_list')

    def getMacroConfig(self, space, page, macro, configId=None, username=None):
        username = username.lower() if username else None
        configInfo = self.findMacroConfig(space, page, macro, configId, username,
            exact_properties=("space", "page", "macro", "configid", "username"))
        if not configInfo:
            q.errorconditionhandler.raiseError("Config does not exist for /%s/%s/%s/%s for user %s" %
                (space, page, macro, configId, username))
        return self.connection.config.get(configInfo[0]['guid'])

    def setMacroConfig(self, space, page, macro, data, configId=None, username=None):
        username = username.lower() if username else None
        configInfo = self.findMacroConfig(space, page, macro, configId, username)
        if not configInfo:
            config = self.connection.config.new()
            config.space = self._getSpaceGuid(space)
            config.page = self._getPageInfo(config.space, page)[0]['guid']
            config.macro = macro
            if configId:
                config.configid = configId
            if username:
                config.username = username
        else:
            config = self.connection.config.get(configInfo[0]['guid'])
        config.data = data
        self.connection.config.save(config)

    def importSpace(self, space, filename, cleanImport = False):
        join = q.system.fs.joinPaths
        import tarfile
        def filterFiler(filename):
            return (filename.startswith("/") or filename.startswith(".."))
        q.logger.log('importing file %s for space %s' % (filename, space), 5)
        tarFile = tarfile.open(filename)
        invalidlinks = filter(filterFiler, tarFile.getnames())
        if invalidlinks:
            #Prepare error message
            if len(invalidlinks) > 15:
                invalidlinks = invalidlinks[:14]
                invalidlinks.append("...")
            raise ValueError("File names must be relative, please remove the following files\n"%"\n".join(invalidlinks))
        dest = self._getDir(space)
        #if the space already exists, I should remove it first
        if self.spaceExists(space) and cleanImport:
            q.system.fs.removeDirTree(dest)
            q.system.fs.createDir(dest)
        tarFile.extractall(join(dest, ""))
        tarFile.close()
        self.syncPortal(space=space)

    def exportSpace(self, space, filename):
        join = q.system.fs.joinPaths
        def buildTree(client, path, space, pagenams = None):
            if not pagenams:
                pagenams = client.listChildPages(space)

            for pagename in pagenams:
                chidpages = client.listChildPages(space, pagename)
                pagepath = join(path, pagename)
                q.system.fs.createDir(pagepath)
                if chidpages:
                    buildTree(client, pagepath, space, chidpages)
                page = client.getPage(space, pagename)
                filename = join(pagepath, pagename + ".md")
                fpage = open(filename, "w")
                fpage.write("@metadata title = %s\n"%page.title)
                fpage.write("@metadata order = %s\n"%page.order)
                fpage.write("@metadata tagstring = %s\n"%str(page.tags))
                fpage.write(page.content)
                fpage.close()

        q.logger.log('exporting space %s to file %s' % (space, filename), 5)
        tempdir = join(q.dirs.tmpDir, space)
        buildTree(self, tempdir, space)
        import tarfile
        tarFile = tarfile.open(filename, mode="w|gz")
        tarFile.add(tempdir, "")
        tarFile.close()
        q.system.fs.removeDirTree(tempdir)

    def hgCheckInfo(self, space, repository, repo_username, repo_password):
        if space.repository.url != repository or space.repository.username != repo_username or \
            (repo_password and space.repository.password != repo_password):

            self.updateSpace(space.guid, repository=repository, repo_username=repo_username,
                repo_password=repo_password)
            return True
        return False

    def createRepoUrl(self, repo):
        from urlparse import urlsplit, urlunsplit
        url = urlsplit(repo.url)
        return urlunsplit((url.scheme, "%s:%s@%s" % (repo.username, repo.password, url.netloc), url.path, url.query,
            url.fragment))

    def hgPushSpace(self, space, repository, repo_username, repo_password=None):
        if not repository:
            return "Please give a repository to push to."

        spaceInfo = self.getSpace(space)

        #check if we need to update the repo in osis
        if self.hgCheckInfo(spaceInfo, repository, repo_username, repo_password):
            #update to reflect changes
            spaceInfo = self.getSpace(space)

        repoUrl = self.createRepoUrl(spaceInfo.repository)

        q.logger.log('pushing space %s to %s' % (spaceInfo.name, spaceInfo.repository.url), 5)

        hg = q.clients.mercurial.getclient(self._getDir(spaceInfo.name), repoUrl)

        #check if we already have the latest version
        retval, msg = hg._hgCmdExecutor("incoming", source=hg.getUrl(), die=False, autoCheckFix=False)
        if retval == 1 and "no changes found" in msg: #no changes we can push
            #set the username for the commit
            hg._ui.environ["HGUSER"] = spaceInfo.repository.username
            hg.addremove('Add new files, and drop deleted files')
            hg.pushcommit("automated commit by Alkira", addRemoveUntrackedFiles=True)
            return True
        else:
            return False

    def hgPullSpace(self, space, repository, repo_username, repo_password=None, dontSync=False):
        if not repository:
            return "Please give a repository to pull from."

        spaceInfo = self.getSpace(space)

        #check if we need to update the repo in osis
        if self.hgCheckInfo(spaceInfo, repository, repo_username, repo_password):
            #update to reflect changes
            spaceInfo = self.getSpace(space)

        repoUrl = self.createRepoUrl(spaceInfo.repository)

        #pull everything
        q.logger.log('pulling space %s from %s' % (spaceInfo.name, spaceInfo.repository.url), 5)
        repoDir = self._getDir(spaceInfo.name)
        cleandir = False
        if self.countPages(space):
            homepage = self.getPage(space, 'Home')
            cleandir = not bool(homepage.content)
            
        hg = q.clients.mercurial.getclient(repoDir, repoUrl, cleandir=cleandir)
        hg.pullupdate()

        #resync pages for space
        if not dontSync:
            self.syncPortal(space=spaceInfo.name)

        return True
    
    def syncPortal(self, path=None, space=None, page=None, cleanup=None):
        def deletePages(space):
                pages = self.pageFind(space=space)
                for page in pages:
                    self.connection.page.delete(page)
        
        def pageDuplicate(page):
            page_name = q.system.fs.getBaseName(page)
            if page_name in page_occured:
                q.errorconditionhandler.raiseError("Another page with the name '%s' already exists on this space. Will NOT create/update the following page (%s)"%(page_name, page))
            else:
                page_occured.append(page_name)
    
        def filterContent(page_content):
            content_dict = {}
            page_lines = page_content.splitlines()
            while len(page_lines) and page_lines[0].startswith('@metadata'):
                meta_line = page_lines.pop(0)
                meta_line = meta_line.replace('@metadata', "")
                meta_list = meta_line.split('=')
    
                header = meta_list[0].strip()
                value = meta_list[1].strip()
    
                content_dict[header] = value
    
            filtered_content = "\n".join(page_lines)
            content_dict['content'] = filtered_content
    
            return content_dict
    
        def createPage(page_file, parent=None):
            pageDuplicate(page_file)
            name = q.system.fs.getBaseName(page_file).split('.')[0]
            content = q.system.fs.fileGetContents(page_file)
            page_info = self.pageFind(name=name, space=spaceguid, exact_properties=("name", "space"))
    
            if len(page_info) > 1:
                raise ValueError('Multiple pages found!')
            elif len(page_info) == 1:
                save_page = functools.partial(self._updatePage, old_name=name)
                q.console.echo('Updating page: %s'%name, indent=4)
            else:
                save_page = self._createPage
                q.console.echo('Creating page: %s'%name, indent=3, withStar=True)
    
            # Setting content and metadata
            page_content_dict = filterContent(content)
            content = page_content_dict.get('content', 'Page is empty.')
            title = page_content_dict.get('title', name)
            order = int(page_content_dict.get('order', '10000'))
    
            # Creating and setting tags
            tags = page_content_dict.get('tagstring', "").split(" ")
            tags = set(tags)
            tags.add('space:%s' % space)
            tags.add('page:%s' % name)
    
            if name == "Home" and spaceobject.name != "Admin":
                self.updateSpace(spaceobject.name, order=int(page_content_dict.get('spaceorder', '1000')))
    
            for tag in re.sub('((?=[A-Z][a-z])|(?<=[a-z])(?=[A-Z]))', ' ', name).strip().split(' '):
                tags.add(tag)
    
            save_page(space=space, name=name, content=content, order=order, title=title, tagsList=tags, category='portal', parent=parent)
    
        def alkiraTree(folder_paths, root_parent=None):
            for folder_path in folder_paths:
                base_name = q.system.fs.getBaseName(folder_path)
                # Ignore hg dir
                if base_name == '.hg':
                    continue
    
                folder_name = base_name.split('.')[0]
                parent_name = folder_name + '.md'
                parent_path = q.system.fs.joinPaths(folder_path, parent_name)
    
                if not q.system.fs.exists(parent_path):
                    q.errorconditionhandler.raiseError('The directory "%s" does not have a page "%s" specified for it.'%(folder_path, parent_name))
    
                if root_parent:
                    createPage(parent_path, parent=root_parent)
                else:
                    createPage(parent_path)
    
                children_files = q.system.fs.listFilesInDir(folder_path, filter='*.md')
                for child_file in children_files:
                    if child_file != parent_path:
                        createPage(child_file, parent=folder_name)
    
                sub_folders = q.system.fs.listDirsInDir(folder_path)
                if sub_folders:
                    alkiraTree(sub_folders, root_parent=folder_name)
    
        md_path = ''
        if not path:
            md_path = q.system.fs.joinPaths(q.dirs.baseDir, 'pyapps', self.api.appname, 'portal', 'spaces')
        else:
            md_path = path
    
        if cleanup:
            deletePages(space)
    
        if space:
            space_dir = q.system.fs.joinPaths(md_path, space)
            if not q.system.fs.exists(space_dir):
                q.errorconditionhandler.raiseError('Space "%s" does not exist.'%space)
            portal_spaces = [space_dir]
        else:
            portal_spaces = q.system.fs.listDirsInDir(md_path)
    
        #make the first space is the Admin Space
        portal_spaces = sorted(portal_spaces, lambda x,y: -1 if x.endswith("/Admin") else 1)
    
        for folder in portal_spaces:
            space = folder.split(os.sep)[-1]
            spaceguid = None
            if space not in self.listSpaces():
                #create space
                self.createSpace(space)
    
            spaceobject = self.getSpace(space)
            spaceguid = spaceobject.guid
    
            q.console.echo('Syncing space: %s' % space)
    
            page_occured = []
    
            if page:
                page_file = q.system.fs.walk(folder, 1, '%s.md' % page)
                if not page_file:
                    q.errorconditionhandler.raiseError("Could not find %s in space %s" % (page, space))
                createPage(page_file[0])
                return
    
            #Special handling for "Imported" space, dont traverse
            if space == IMPORTSPACE:
                folder_paths = list()
            else:
                folder_paths = q.system.fs.listDirsInDir(folder)
            main_files = q.system.fs.listFilesInDir(folder, filter='*.md')
    
            for each_file in main_files:
                createPage(each_file)
    
            alkiraTree(folder_paths)
        