# @task - MNour: Clean unused code.
from pylabs import q, p

import os
import urllib
import inspect
import re
import functools
import httplib
import oauth2
import json
import ast

ADMINSPACE = "Admin"
IDESPACE = "IDE"

class Alkira(object):
    def __init__(self):
        """
        Initialize the alkira library with a certain Service

        @param service: Application Server service using this Alkira library
        @type service:  Application Server service
        """
        self.KNOWN_TYPES = ["py", "md", "html", "txt"]
        self._serializer = q.db.pymodelserializers.thriftbase64
        self._deserializer = q.db.pymodelserializers.thriftbase64

    def _callAuthService(self, method, oauthInfo, **args):
        data = {}
        #only pass arguments that has value
        for k, v in args.iteritems():
            if v != None:
                data[k] = json.dumps(v)

        headers = {'Content-Type': "application/x-www-form-urlencoded"}

        url = '/%(appname)s/appserver/rest/ui/auth/%(method)s' % {'appname': self.api.appname, 'method': method}

        httpMethod = "POST"

        if oauthInfo and "token" in oauthInfo and "username" in oauthInfo:
            arakoon = q.clients.arakoon.getClient(self.api.appname)
            if arakoon.exists(key=oauthInfo["token"]):
                tokenAttributes = arakoon.get(oauthInfo["token"])
                if tokenAttributes:
                    tokenAttributes = ast.literal_eval(tokenAttributes)
                if tokenAttributes:
                    #remove the appname from the call ass the appserver doesn't get this in his request
                    oauthUrl = url[len("/%s" % self.api.appname):]

                    consumer = oauth2.Consumer(oauthInfo["username"], "")
                    token = oauth2.Token(oauthInfo["token"], tokenAttributes["tokensecret"])
                    req = oauth2.Request.from_consumer_and_token(consumer, token, http_method=httpMethod,
                        http_url="http://alkira%s" % oauthUrl, parameters=data)
                    req.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
                    oauthHeaders = req.to_header(realm="alkira")
                    headers.update(oauthHeaders)

        data = urllib.urlencode(data)
        con = httplib.HTTPConnection("localhost", 80)
        try:
            con.request(httpMethod, url, body=data, headers=headers)
            res = con.getresponse()
            result = res.read()
            try:
                body = json.loads(result)
            except ValueError:
                body = result
            if res.status == 200:
                return body
            else:
                raise Exception(body['exception'] if 'exception' in body else res.reason, res.status)
        finally:
            con.close()

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

    def _getProjectGuid(self, project):
        if isinstance(project, basestring):
            if q.basetype.guid.check(project):
                return project
            else:
                projects = self._getProjectInfo(project)
                if not projects:
                    q.errorconditionhandler.raiseError("Project %s does not exist." % project)
                return projects[0]['guid']
        elif isinstance(project, self.connection.project._ROOTOBJECTTYPE):
            return project.guid

    def _getSpaceInfo(self, name=None):
        filter = self.connection.space.getFilterObject()
        if name:
            filter.add('ui_view_space_list', 'name', name, True)
        space = self.connection.space.findAsView(filter, 'ui_view_space_list')
        return space

    def _getProjectInfo(self, name=None):
        filter = self.connection.project.getFilterObject()
        if name:
            filter.add('ui_view_project_list', 'name', name, True)
        project = self.connection.project.findAsView(filter, 'ui_view_project_list')
        return project

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

    def search(self, text=None, tags=None):
        # ignore tags for now

        if not any([text, tags]):
            return []

        sql_select = '"index"."name", "index".url'
        sql_from = 'ui__index.global_index_view as "index"'
        sql_where = ['1=1']

        if tags:
            tags = urllib.unquote_plus(tags)
            tags = tags.strip(', ')
            sql_where.append('"index".tags LIKE \'%%%s%%\'' %  tags)

        if text:
            sql_where.append('"index".content LIKE \'%%%s%%\'' % text)

        query = 'SELECT %s FROM %s WHERE %s' % (sql_select, sql_from, ' AND '.join(sql_where))

        result = self.connection._index.query(query)

        return result

    def listProjects(self):
        """
        List all projects
        """
        return map(lambda item: item["name"],
                   self.listProjectInfo())

    def listProjectInfo(self, name=None):
        """
        List projects info
        """
        return self._getProjectInfo(name)

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
            #Always put the admin and ide spaces last if they don't have an order or if the order is set to None
            if (x["name"] == ADMINSPACE or x["name"] == IDESPACE) and ("order" not in x or x["order"] is None):
                return 1
            elif (y["name"] == ADMINSPACE or y["name"] == IDESPACE) and ("order" not in y or y["order"] is None):
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

    def spaceExists(self, service, space):
        """
        Checks whether a space exists or not

        @param service: Service with which this library is used
        @type service:  Application Server service
        @param space: Space name
        @type space:  string

        @return: True if the space exists, False otherwise
        """
        space_prefixed_keys = service.db.prefix(space)
        return space_prefixed_keys not in (None, [])

    def projectExists(self, name):
        """
        Checks whether a project exists or not

        @param name: Project name

        @return: True if the project exists, False otherwise
        """
        return bool(self._getProjectInfo(name))

    def pageExists(self, service, space, name):
        """
        Checks whether a page exists or not.

        @type space: String
        @param space: The name of the space.

        @type name: String
        @param name: The name of the page.

        @return: True if the page exists, False otherwise.
        """
        if not service:
            raise Exception('Invalid Service reference.')

        if not space or not name:
            raise ValueError('Invalid space or name values. Space: %s, Name: %s' % (space, name))

        page_id = service.extensions.common.alkira.getPageId(space, name)
        space_prefixed_keys = service.db.prefix(space)
        if space_prefixed_keys:
            return page_id in space_prefixed_keys

        return False

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

    def userFind(self, name='', exact_properties=None):
        filterObject = self.connection.user.getFilterObject()
        exact_properties = exact_properties or ()

        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)

        properties = ('name')
        for property_name, value in values.iteritems():
            if property_name in properties and not value in (None, ''):
                exact = property_name in exact_properties
                filterObject.add('ui_view_page_list', property_name, value, exactMatch=exact)

        return self.connection.user.find(filterObject)

    def getProject(self, project):
        """
        Gets a project object

        @param project: The project name, or guid
        """
        if isinstance(project, self.connection.project._ROOTOBJECTTYPE):
            return project

        guid = self._getProjectGuid(project)
        return self.connection.project.get(guid)

    def getSpace(self, service, space):
        """
        Gets a space object

        @param service: The service with which this library used
        @type service:  Application Server service
        @param space: The space name, or guid
        @type space:  string or guid
        """
        # @task - MNour: - I don't like the _ROOTOBJECTTYPE. I wanna change it to something better.
        #                - Look at pylabs-core-5.1/extensions/baseworking/db/pymodel_extension/pymodel_extension.py
        if isinstance(space, service.model.space._ROOTOBJECTTYPE):
            return space

        space = self._getSpaceGuid(space)
        return self.connection.space.get(space)

    def getPage(self, service, space, name):
        """
        Gets a page object.

        @param service: Service with which this library is used
        @type service:  Application Service service
        @type space:    string
        @param space:   space name
        @type name:     string
        @param name:    page name

        @return: Page object.
        """
        page_id = service.extensions.common.alkira.getPageId(space, name)        
        if not service.db.exists(page_id):
            q.errorconditionhandler.raiseError('Page %s does not exist.' % name)
        serialized_page = service.db.get(page_id)
        # @remark - MNour: I know _ROOTOBJECTTYPE is not nice but I will change it later
        return self._deserializer.deserialize(service.model.page._ROOTOBJECTTYPE, serialized_page)

    def getPageByGUID(self, guid):
        """
        Get a page object by guid

        @param guid: Page guid
        """

        return self.connection.page.get(guid)

    def deleteProject(self, project):
        """
        Delete a project

        @param project: Project name of GUID
        """
        guid = self._getProjectGuid(project)
        self.connection.project.delete(guid)

    def deleteSpace(self, space):
        """
        Delete space

        @param space: The space name, object or guid to delete

        @note: Deleting a space will delete all the pages in that space.
        """
        if space in (ADMINSPACE, IDESPACE):
            raise ValueError("%s space is not deletable" % space)

        space = self.getSpace(space)

        pages = self.listPageInfo(space)

        for page in pages:
            self.connection.page.delete(page['guid'])

        self.connection.space.delete(space.guid)
        spacefile = 's_' + space.name
        self.deletePage(ADMINSPACE, spacefile)
        q.system.fs.removeDirTree(self._getDir(space.name))

    def _syncPageToDisk(self, space, page, oldpagename=None):
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

                    if _isfile(oldfile):
                        self._moveFile(oldfile, tofile)
                    if _isdir(olddir):
                        self._moveDir(olddir, dir)

                _write(file, page.content)
            else:
                if not _isdir(dir):
                    q.system.fs.createDir(dir)

            upper = dir

    def _syncPageDelete(self, space, crumbs):
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
                if _isfile(file):
                    q.system.fs.removeFile(file)

    def _deletePage(self, service, space, page):
        # def deleterecursive(guid):
        #     filter = self.connection.page.getFilterObject()
        #     filter.add("ui_view_page_list", "parent", guid, True)

        #     for chguid in self.connection.page.find(filter):
        #         deleterecursive(chguid)

        #     self.connection.page.delete(guid)

        # @remark - MNour: Coming back to that later
        # crumbs = self._breadcrumbs(page)
        # deleterecursive(page.guid)
        # self._syncPageDelete(space, crumbs)
        page_id = service.extensions.common.alkira.getPageId(space, page.name)
        service.db.delete(page_id)

    def deletePageByGUID(self, guid):
        """
        Delete a page by guid

        @param guid: page guid
        """
        """
        Deletes a page and its chlidren (recursively).

        @type guid: GUID
        @param guid: Page guid
        """
        page = self.getPageByGUID(guid)
        space = self.getSpace(page.space)
        self._deletePage(space.name, page)

    def deletePage(self, service, space, name):
        page = self.getPage(service, space, name)
        self._deletePage(service, space, page)

    def createSpace(self, name, tagsList=[], repository="", repo_username="", repo_password="", order=None, createHomePage=True):
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
        spacefile = 's_' + name
        spacectnt = p.core.codemanagement.api.getSpacePage(name)
        if createHomePage:
            self.createPage(name, "Home", content="", order=10000, title="Home", tagsList=tagsList)
        self.createPage(ADMINSPACE, spacefile, spacectnt, title=name, parent="Spaces")

        return space

    def createProject(self, name, path, tagsList=[]):
        """
        Create a new project

        @param name: Name of the project
        @param path: Relative path of the project files (relative from the pyapp location)
        """
        if self.projectExists(name):
            q.errorconditionhandler.raiseError("Project %s already exists." % name)

        project = self.connection.project.new()
        project.name = name
        project.path = path
        project.tags = ' '.join(tagsList)

        self.connection.project.save(project)
        return project

    def updateProject(self, project, newname=None, path=None, tagsList=None):
        """
        Update project

        @param project: Project name or guid
        @param newname: New project name
        @param path: set project path
        @param tagsList: New project tags list
        """
        project = self.getProject(project)

        if newname:
            project.name = newname
        if path:
            project.path = path
        if tagsList != None:
            project.tags = ' '.join(tagsList)

        self.connection.project.save(project)
        return project

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
        return self._breadcrumbs(self.getPage(space, name))

    def _createPage(self, service, space, name, content, order=None, title=None, tagsList=[], category='portal',
                   parent=None, filename=None, contentIsFilePath=False, pagetype="md"):
        # @remark - MNour: Make it simple for now. Just use string space names, no objects, no guids.
        # space = self.getSpace(space)
        if self.pageExists(service, space, name):
            q.errorconditionhandler.raiseError('Page %s already exists.' % name)

        page = service.model.page.getEmptyModelObject()
        params = {
                  # @remark - MNour: I am not using GUID(s) for now
                  # 'name':name, 'pagetype': pagetype, 'space':space.guid, 'category':category, 'title': title,
                  'name':name, 'pagetype': pagetype, 'category':category, 'title': title,
                  'order': order, 'filename':filename,
                  'content':q.system.fs.fileGetContents(content) if contentIsFilePath else content
                 }
        for key in params:
            if params[key] != None:
                setattr(page, key, params[key])

        if not order:
            page.order = 10000

        tags = set(tagsList)
        # @remark - MNour: Spaces are only strings for now
        # tags.add('space:%s' % space.name)
        tags.add('space:%s' % space)
        tags.add('page:%s' % name)
        page.tags = ' '.join(tags)

        # @task - MNour: Support parent pages later.
        # if parent:
        #     parent_page = self.getPage(space.guid, parent)
        #     page.parent = parent_page.guid

        page_id = service.extensions.common.alkira.getPageId(space, name)
        service.db.set(page_id, page.serialize(self._serializer))
        # @remark - MNour: For now guids are not set yet.
        return page

    def createPage(self, service, space, name, content, order=None, title=None, tagsList=[], category='portal', parent=None,
                   filename=None, contentIsFilePath=False, pagetype="md"):
        """
        Creates a new page.

        @param service:           Service with which this library is used
        @type service:            Application Server service
        @type space:              string
        @param space:             The name of the space.
        @type name:               string
        @param name:              The name of the page.
        @type content:            string
        @param content:           The content of the page. This can also be a file path; in this case you should set contentIsFilePath=True.
        @type order:              integer
        @param order:             Order of the page
        @type title:              string
        @param title:             Title of the page
        @type tagsList:           list
        @param tagsList:          A list containing all the tags you want to add to the page.
        @type category:           String
        @param category:          The category of the page. Default is 'portal'.
        @type parent:             string
        @param parent:            If you want this to become a child page, add the name of the parent page to this parameter. Default is None.
        @type contentIsFilePath:  Boolean
        @param contentIsFilePath: If the content you gave is a file path, set this value to True. Default is False.
        @type filename:           string
        @param filename:          Used by import directory script to store original file path
        """
        # @remark - MNour: Keep the model simple for now. Just use strings.
        # @question - MNour: In that case do we still need to maintain the old model ?
        # space = self.getSpace(service, space)
        page = self._createPage(service, space=space, name=name, content=content, order=order, title=title,
                                tagsList=tagsList, category=category, parent=parent, filename=filename,
                                contentIsFilePath=contentIsFilePath, pagetype=pagetype)
        # @task - MNour: Work on file system syncing later
        # self._syncPageToDisk(space.name, page)
        return page

    def updateSpace(self, space, newname=None, tagslist=None, repository=None, repo_username=None, repo_password=None, order=None):
        space = self.getSpace(space)

        # Allow the modification of the order attribute for Admin and IDE spaces:
        if (space.name == ADMINSPACE or space.name == IDESPACE) and (newname or tagslist or repository or repo_username or repo_password):
            raise ValueError("You can only modify the order for %s space" %space.name)
        
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
            newspacefile = 's_' + newname
            oldspacefile = 's_' + oldname
            self.updatePage(space = ADMINSPACE, old_name = oldspacefile, name=newspacefile, content=p.core.codemanagement.api.getSpacePage(newspacefile))

            #sync file system
            self._moveDir(self._getDir(oldname),
                          self._getDir(newname))

        return space

    def _updatePage(self, space, old_name, name=None, tagsList=None, content=None,
                   order=None, title=None, parent=None, category=None, pagetype=None, filename=None, contentIsFilePath=False):

        space = self.getSpace(space)
        page = self.getPage(space.guid, old_name)

        params = {"name": name, "pagetype": pagetype, "category":category,
                  "title": title, "order": order, "filename":filename,
                  "content":q.system.fs.fileGetContents(content) if contentIsFilePath else content
                  }

        for key in params:
            if params[key] != None:
                setattr(page, key, params[key])

        if tagsList:
            page.tags = ' '.join(tagsList)

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


        self._syncPageToDisk(space.name, page, old_name)

        return page

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
        configInfo = self.findMacroConfig(space, page, macro, configId, username,
            exact_properties=("space", "page", "macro", "configid", "username"))
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

    def getitems(self, prop, space=None, term=None):
        SQL_PAGES = 'SELECT DISTINCT ui_page.ui_view_page_list.%(prop)s FROM ui_page.ui_view_page_list %(space_criteria)s'
        SQL_PAGES_FILTER = 'SELECT DISTINCT ui_page.ui_view_page_list.%(prop)s FROM ui_page.ui_view_page_list WHERE ui_page.ui_view_page_list.%(prop)s LIKE \'%(term)s%%\'  %(space_criteria)s'
        SQL_PAGE_TAGS = 'SELECT DISTINCT ui_page.ui_view_page_list.%(prop)s FROM ui_page.ui_view_page_list WHERE ui_page.ui_view_page_list.space=\'%(space)s\''
        SQL_PAGE_TAGS_FILTER = 'SELECT DISTINCT ui_page.ui_view_page_list.%(prop)s FROM ui_page.ui_view_page_list WHERE ui_page.ui_view_page_list.space=\'%(space)s\' AND ui_page.ui_view_page_list.%(prop)s LIKE \'%%%(term)s%%\''

        if space:
            space = self.getSpace(space)
        t = term.split(', ')[-1] if term else ''

        d = {'prop': prop, 'space': space.guid, 'term': t}
        if prop in ('tags',):
            sql = SQL_PAGE_TAGS_FILTER % d if t else SQL_PAGE_TAGS % d
        else:
            if t:
                d['space_criteria'] = 'AND ui_view_page_list.space = \'%s\'' % space.guid if space else ''
                sql = SQL_PAGES_FILTER % d
            else:
                d['space_criteria'] = 'WHERE ui_view_page_list.space = \'%s\'' % space.guid if space else ''
                sql = SQL_PAGES % d

        qr = self.connection.page.query(sql)
        result = map(lambda _: _[prop], qr)
        return result

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
                parent_dir = q.system.fs.getParent(folder_path)
                parent_path = q.system.fs.joinPaths(parent_dir, parent_name)

                if not q.system.fs.exists(parent_path):
                    q.errorconditionhandler.raiseError(\
                        'The directory "%s" does not have a page "%s" specified for it.' % (parent_dir, parent_name))

                base_name += ".md"
                children_files = q.system.fs.listFilesInDir(folder_path, filter='*.md')
                for child_file in children_files:
                    if q.system.fs.getBaseName(child_file) != base_name:
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
        portal_spaces = sorted(portal_spaces, lambda x,y: -1 if x.endswith("/" + ADMINSPACE) else 1)

        for folder in portal_spaces:
            space = folder.split(os.sep)[-1]
            spaceguid = None
            if space not in self.listSpaces():
                #create space
                self.createSpace(space, createHomePage=False)

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

            folder_paths = q.system.fs.listDirsInDir(folder)
            main_files = q.system.fs.listFilesInDir(folder, filter='*.md')

            for each_file in main_files:
                createPage(each_file)

            alkiraTree(folder_paths)

    def _getUserInfo(self, login=None):
        searchfilter = self.connection.user.getFilterObject()
        if login:
            searchfilter.add('ui_view_user_list', 'login', login, True)
        user = self.connection.user.findAsView(searchfilter, 'ui_view_user_list')
        return user

    def listUsers(self, login=None):
        return map(lambda item: item["login"], self.listUserInfo(login))

    def listUserInfo(self, login=None):
        return self._getUserInfo(login)

    def listUsersInfo(self):
        usersInfo = []
        users = self._getUserInfo()
        for user in users:
            usersInfo.append({"name": user["name"], "guid": user["guid"], \
                "groups": filter(None, user["groupguids"].split(";"))})
        return usersInfo

    def createUser(self, login, name=None, password=None, oauthInfo=None):
        userInfo = {"login": login, "name": name if name else login}
        if password:
            userInfo["password"] = password
        return self._callAuthService("createUser", oauthInfo, userinfo=userInfo)

    def updateUser(self, userguid, name=None, password=None, oauthInfo=None):
        userinfo = {}
        if name:
            userinfo["name"] = name
        if password:
            userinfo["password"] = password

        if userinfo:
            return self._callAuthService("updateUser", oauthInfo, userid=userguid, userinfo=userinfo)
        return False

    def deleteUser(self, userguid, oauthInfo=None):
        return self._callAuthService("deleteUser", oauthInfo, userid=userguid)

    def getUser(self, name):
        user_info = self._getUserInfo(name)
        if not user_info:
            q.errorconditionhandler.raiseError("User %s does not exist." % name)
        return self.connection.user.get(user_info[0]['guid'])

    def getUserGroups(self, name):
        searchfilter = self.connection.user.getFilterObject()
        searchfilter.add('ui_view_user_list', 'login', name, True)
        user = self.connection.user.findAsView(searchfilter, 'ui_view_user_list')
        if user and len(user) == 1:
            return filter(None, user[0]["groupguids"].split(";"))

    def addUserToGroup(self, userguid, groupguid, oauthInfo=None):
        return self._callAuthService("addUserToGroup", oauthInfo, userid=userguid, usergroupid=groupguid)

    def removeUserFromGroup(self, userguid, groupguid, oauthInfo=None):
        return self._callAuthService("deleteUserFromGroup", oauthInfo, userid=userguid, usergroupid=groupguid)

    def createGroup(self, name, oauthInfo=None):
        groupInfo = {"name": name}
        return self._callAuthService("createUsergroup", oauthInfo, usergroupinfo=groupInfo)

    def _getGroupInfo(self, name=None):
        searchfilter = self.connection.group.getFilterObject()
        if name:
            searchfilter.add('ui_view_group_list', 'name', name, True)
        group = self.connection.group.findAsView(searchfilter, 'ui_view_group_list')
        return group

    def deleteGroup(self, groupguid, oauthInfo=None):
        return self._callAuthService("deleteUsergroup", oauthInfo, usergroupid=groupguid)

    def updateGroup(self, groupguid, name):
        group = self.connection.group.get(groupguid)
        group.name = name
        self.connection.group.save(group)
        return group.guid

    def listGroupsInfo(self):
        groupsInfo = []
        groups = self._getGroupInfo()
        for group in groups:
            groupsInfo.append({"name": group["name"], "guid": group["guid"]})
        return groupsInfo

    def listGroups(self, name):
        return map(lambda item: item["name"], self._getGroupInfo(name))

    def assignRule(self, groupguids, function, context, oauthInfo=None):
        return self._callAuthService("authorise", oauthInfo, groups=groupguids, functionname=function, context=context)

    def _getRuleInfo(self, groupguid=None, function=None, context=None):
        searchfilter = self.connection.authoriserule.getFilterObject()
        if groupguid:
            searchfilter.add('ui_view_authoriserule_list', 'groupguids', ";" + groupguid + ";", False)
        if function:
            searchfilter.add('ui_view_authoriserule_list', 'function', function, True)
        if context:
            searchfilter.add('ui_view_authoriserule_list', 'context', context, True)
        rule = self.connection.authoriserule.findAsView(searchfilter, 'ui_view_authoriserule_list')
        return rule

    def revokeRule(self, groupguids, function, context, oauthInfo=None):
        return self._callAuthService("unAuthorise", oauthInfo, groups=groupguids, functionname=function, \
            context=context)

    def listRulesInfo(self):
        rulesInfo = []
        rules = self._getRuleInfo()
        for rule in rules:
            rulesInfo.append({"name": rule["guid"], "guid": rule["guid"], \
                "groups": filter(None, rule["groupguids"].split(";")), \
                "function": rule["function"], "context": rule["context"]})
        return rulesInfo

    def createDefaultRules(self):
        try:
            adminGuid = self.createUser("admin", "Admin User", "admin")
        except:
            return

        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "auth_backend"))
        authbackend = __import__("authbackend", level=1)

        adminsGuid = self._getGroupInfo(getattr(authbackend, "ADMIN_GROUP"))[0]["guid"]
        self.addUserToGroup(adminGuid, adminsGuid)

        publicGroupGuid = self._getGroupInfo(getattr(authbackend, "PUBLIC_GROUP"))[0]["guid"]
        pageCreatorsGuid = self.createGroup("Page Creators")
        pageEditorsGuid = self.createGroup("Page Editors")
        developersGuid = self.createGroup("Developers")

        def assignRuleTryCatch(groups, function, context):
            try:
                self.assignRule(groups, function, context)
            except:
                pass

        def assignRules(rules):
            for rule in rules:
                if not "defaultGroups" in rule:
                    continue
                if not "authorizeRule" in rule:
                    continue

                if "admin" in rule["defaultGroups"]:
                    assignRuleTryCatch([adminsGuid], rule["authorizeRule"], {})
                if "public" in rule["defaultGroups"]:
                    assignRuleTryCatch([publicGroupGuid], rule["authorizeRule"], {})
                if "creator" in rule["defaultGroups"]:
                    assignRuleTryCatch([pageCreatorsGuid], rule["authorizeRule"], {})
                if "editor" in rule["defaultGroups"]:
                    assignRuleTryCatch([pageEditorsGuid], rule["authorizeRule"], {})
                if "developer" in rule["defaultGroups"]:
                    assignRuleTryCatch([developersGuid], rule["authorizeRule"], {})


        from lfw import LFWService
        assignRules(LFWService.getAuthorizedFunctions())

        from authservice import AuthService
        assignRules(AuthService.getAuthorizedFunctions())

        from ide import ide
        assignRules(ide.getAuthorizedFunctions())

