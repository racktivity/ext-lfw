from pylabs import q, p

import os
import urllib
import inspect
import re
import functools
import time
import sqlalchemy
from .authservice import AuthService

# HACK - to be removed
# Used for locking access to create page function in order to prevent creation of duplicate pages
import locklib

ADMINSPACE = "Admin"
IDESPACE = "IDE"

class Alkira:
    def __init__(self, api=None):
        """
        Initialize the alkira library with a certain API

        @param api: The application api (in APPSERVER content)
        """
        self.KNOWN_TYPES = ["py", "md", "html", "txt"]

        self.connection = api.model.ui
        self.osis = p.application.getOsisConnection(api.appname)
        self.api = api
        self.authService = None

    def _callAuthService(self, method, oauthInfo=None, **args): #pylint: disable=W0613
        if self.authService is None:
            self.authService = AuthService()

        func = getattr(self.authService, method)
        return func(**args)

    def _getPageInfo(self, space, name):
        page_filter = self.connection.page.getFilterObject()
        page_filter.add('page', 'name', name, True)
        page_filter.add('page', 'space', space, True)
        page_info = self.connection.page.findAsView(page_filter, 'page')
        return page_info

    def _getSpaceGuid(self, space):
        if isinstance(space, basestring):
            if q.basetype.guid.check(space): #pylint: disable=E1103
                return space
            else:
                spaces = self._getSpaceInfo(space)
                if not spaces:
                    q.errorconditionhandler.raiseError("Space %s does not exist." % space)
                return spaces[0]['guid']
        elif isinstance(space, self.connection.space._ROOTOBJECTTYPE): #pylint: disable=W0212
            return space.guid

    def _getProjectGuid(self, project):
        if isinstance(project, basestring):
            if q.basetype.guid.check(project): #pylint: disable=E1103
                return project
            else:
                projects = self._getProjectInfo(project)
                if not projects:
                    q.errorconditionhandler.raiseError("Project %s does not exist." % project)
                return projects[0]['guid']
        elif isinstance(project, self.connection.project._ROOTOBJECTTYPE): #pylint: disable=W0212
            return project.guid

    def _getSpaceInfo(self, name=None):
        _filter = self.connection.space.getFilterObject()
        if name:
            _filter.add('space', 'name', name, True)
        space = self.connection.space.findAsView(_filter, 'space')
        return space

    def _getProjectInfo(self, name=None):
        _filter = self.connection.project.getFilterObject()
        if name:
            _filter.add('project', 'name', name, True)
        project = self.connection.project.findAsView(_filter, 'project')
        return project

    def _getParentGUIDS(self, guid_list):
        parent_list = list()
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

    def _removeJsHtmlMd(self, data):
        # Remove Js Code enclosed in <script> tags:
        removeJS = re.compile(r"""<script.*>.*</script>""", re.DOTALL)
        data = removeJS.sub('', data)

        # Remove Js Code enclosed in [[script]] tags:
        removeJsFromMd = re.compile(r"""\[\[script.*\]\].*\[\[/script\]\]""", re.DOTALL)
        data = removeJsFromMd.sub('', data)

        # Remove all mark-down tags:
        removeMD = re.compile(r"""(\[\[.*\]\].*\[\[/.*\]\])|\[\[.*/\]\]""", re.DOTALL)
        data = removeMD.sub('', data)

        # Remove all HTML tags:
        removeHTML = re.compile(r"""<.*>""")
        data = removeHTML.sub('', data)

        # Remove trailing spaces:
        removeSpaces = re.compile(r"""\s*$""")
        data = removeSpaces.sub('', data)

        # Replace all newline characters with whitespaces:
        replaceNl = re.compile(r"""\n""")
        return replaceNl.sub(' ', data)

    #rename doesn't work accross different mount points but has higher performance, so we implemented this move functions
    def _moveFile(self, filePath, new_name):
        try:
            q.system.fs.renameFile(filePath, new_name)
        except: #pylint: disable=W0702
            q.system.fs.moveFile(filePath, new_name)

    def _moveDir(self, filePath, new_name):
        try:
            q.system.fs.renameDir(filePath, new_name)
        except: #pylint: disable=W0702
            q.system.fs.moveDir(filePath, new_name)

    def listPages(self, space=None):
        """
        Lists all the pages in a certain space.

        @param space: The name, guid or space object of the space.
        """
        return map(lambda i: i['name'], self.listPageInfo(space)) #pylint: disable=W0141

    def listFilteredTitles(self, space=None, term=None):
        """
        Lists pages in a certain space, filtering title with term.

        @param space: The name, guid or space object of the space.
        @param term: string to filter titles.
        """
        ret = list()
        pages = self.listPageInfo(space)
        for page in pages:
            if page['title'].lower().find(term.lower()) != -1:
                ret.append(page['title'])
        return ret

    def countPages(self, space=None):
        page = self.osis.findTable("ui", "page")
        select = sqlalchemy.select([ sqlalchemy.func.count(page.c.guid) ])
        if space:
            space = self._getSpaceGuid(space)
            select.where(page.c.space == space)

        return self.osis.runSqlAlchemyQuery(select).fetch_one()[0]

    def _splitSearchString(self, text):
        wordList = list()

        # First find all phrases enclosed in double quotes:
        phrasesList = re.findall("\".*?\"", text)
        for phrase in phrasesList:
            wordList.append(phrase[1:-1])

        # Remove all previously detected phrases from the text and the remaining
        # double quotes, then split the remaining text into words:
        text = re.sub("\".*?\"", " ", text)
        text = re.sub("\"", "", text)
        wordList.extend(text.split())

        return wordList

    def search(self, text=None, tags=None, title=None, query=None, qtype=None):
        CONTENT_MAX_LENGTH = 100

        index = self.osis.findTable("ui", "_index")

        columns = [ index.c.name, index.c.url, index.c.content, index.c.description ]
        where = list()

        # new way of handling search request brings type to determine
        # how to search
        if qtype == 'simple':
            query = str(query)

            if not query:
                return list()

            # Replace \x07 characters back with double quotes since the enclosed double quotes
            # are removed in the applicationserver if they are not encoded like this:
            query = query.replace('\x07', '"')

            # Search string is considered a phrase if enclosed in double quotes,
            # otherwise each word from the string will be searched:
            query = urllib.unquote_plus(query).lower()
            wordList = self._splitSearchString(query)
            for word in wordList:
                # Each word should be found in at least one of those three db fields:
                where.append(sqlalchemy.or_(
                    index.c.content.ilike('%%%s%%' % word),
                    index.c.tags.ilike('%%%s%%' % word),
                    index.c.name.ilike('%%%s%%' % word)
                ))
        else:
            # here we go with extended search that also can work as old-style search (no type)
            text = str(text)
            if not any([text, tags, title]):
                return list()

            if tags:
                tags = urllib.unquote_plus(tags)
                tags = tags.strip(', ')
                where.append(index.c.tags.ilike('%%%s%%' % tags.lower()))

            if text:
                where.append(index.c.content.ilike('%%%s%%' % text.lower()))
            if title:
                where.append(index.c.name.ilike('%%%s%%' % title.lower()))

        select = sqlalchemy.select(columns, whereclause=sqlalchemy.and_(*where))
        qr = self.osis.runSqlAlchemyQuery(select)

        # If description is present then use it, otherwise use page content:
        result = []
        for item in qr:
            item = dict(item)
            if item['description'] != None:
                item['content'] = item['description']
            elif item['content'] != None:
                # Get rid of the HTML/mark-down tags and JS code:
                item['content'] = self._removeJsHtmlMd(item['content'])
                if len(item['content']) > CONTENT_MAX_LENGTH:
                    item['content'] = item['content'][:CONTENT_MAX_LENGTH] + '...'
            del item['description']
            result.append(item)

        return result

    def listProjects(self):
        """
        List all projects
        """
        return map(lambda item: item["name"], self.listProjectInfo()) #pylint: disable=W0141

    def listProjectInfo(self, name=None):
        """
        List projects info
        """
        return self._getProjectInfo(name)

    def listSpaces(self):
        """
        Lists all the spaces.
        """
        return map(lambda item: item["name"], self.listSpaceInfo()) #pylint: disable=W0141

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
        _filter = self.connection.page.getFilterObject()
        if space:
            space = self._getSpaceGuid(space)
            _filter.add('page', 'space', space, True)

        return self.connection.page.findAsView(_filter, 'page')

    def listChildPages(self, space, name = None):
        """
        Lists child pages of page "name"

        @type space: String
        @param space: The name of the space.

        @type name: String
        @param name: The name of the parent page.
        """
        space = self._getSpaceGuid(space)
        filterObj = self.connection.page.getFilterObject()
        filterObj.add('page', 'space', space, True)
        #Get page guid
        if name:
            guid = self._getPageInfo(space, name)[0]["guid"]
            filterObj.add('page', 'parent', guid, True)
        else:
            filterObj.add('page', 'parent', None, True)

        query = self.connection.page.findAsView(filterObj, 'page')
        return list(name["name"] for name in query)

    def spaceExists(self, name):
        """
        Checks whether a space exists or not

        @param name: Space name

        @return: True if the space exists, False otherwise
        """
        return bool(self._getSpaceInfo(name))

    def projectExists(self, name):
        """
        Checks whether a project exists or not

        @param name: Project name

        @return: True if the project exists, False otherwise
        """
        return bool(self._getProjectInfo(name))

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

    def pageFind(self, name='', space='', category='', parent='', tags='', order=None, title='', exact_properties=None): #pylint: disable=W0613
        filterObject = self.connection.page.getFilterObject()
        exact_properties = exact_properties or ()

        space = self._getSpaceGuid(space) if space else ''
        frame = inspect.currentframe()
        _, _, _, values = inspect.getargvalues(frame)

        properties = ('name', 'space', 'category', 'parent', 'tags', 'order', 'title')
        for property_name, value in values.iteritems():
            if property_name in properties and not value in (None, ''):
                exact = property_name in exact_properties
                filterObject.add('page', property_name, value, exactMatch=exact)

        return self.connection.page.find(filterObject)

    def userFind(self, name='', exact_properties=None): #pylint: disable=W0613
        filterObject = self.connection.user.getFilterObject()
        exact_properties = exact_properties or ()

        frame = inspect.currentframe()
        _, _, _, values = inspect.getargvalues(frame)

        properties = ('name')
        for property_name, value in values.iteritems():
            if property_name in properties and not value in (None, ''):
                exact = property_name in exact_properties
                filterObject.add('page', property_name, value, exactMatch=exact)

        return self.connection.user.find(filterObject)

    def getProject(self, project):
        """
        Gets a project object

        @param project: The project name, or guid
        """
        if isinstance(project, self.connection.project._ROOTOBJECTTYPE): #pylint: disable=W0212
            return project

        guid = self._getProjectGuid(project)
        return self.connection.project.get(guid)

    def getSpace(self, space):
        """
        Gets a space object

        @param name: The space name, or guid
        """
        if isinstance(space, self.connection.space._ROOTOBJECTTYPE): #pylint: disable=W0212
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

    def _syncPageToDisk(self, space, page, oldpagename=None, oldPageObject = None):
        """
        this method writes the content's page to disk
        the parameter oldPageObject is only used when a page is updated
        @params space : string that represents the space name:, example View
        @type   space : string
        @params page  : object page
        @type   page  : object
        @params oldpagename : string that represents the page name(this is currently a guid)
        @type   oldpagename : string
        @params oldPageObject : object that represents the old page, in case of updating a page
        @type   oldPageObject : object
        """

        olddir = None
        oldfile = None
        if oldPageObject:
            if page.parent != oldPageObject.parent:
                oldfile  = self.getPageLocation(space, oldPageObject)
                basedir  = q.system.fs.getDirName(oldfile)
                basename = q.system.fs.getBaseName(oldfile)
                olddir   = q.system.fs.joinPaths(basedir, os.path.splitext(basename)[0])
            else:
                oldPageObject = None

        crumbs = self._breadcrumbs(page)
        _join = q.system.fs.joinPaths
        _isfile = q.system.fs.isFile
        _isdir = q.system.fs.isDir
        _write = q.system.fs.writeFile

        _dir = self._getDir(space)
        upper = _dir
        for i, level in enumerate(crumbs):
            name = level['name']
            filename = name + ".md"
            _file = _join(_dir, filename)
            _dir = _join(_dir, name)

            if i == len(crumbs) - 1:
                if oldpagename and not oldPageObject:
                    oldfile = _join(upper, oldpagename + ".md")
                    olddir = _join(upper, oldpagename)

                if olddir:
                    if _isfile(oldfile):
                        self._moveFile(oldfile, _file)
                    if _isdir(olddir):
                        self._moveDir(olddir, _dir)

                _write(_file, page.content)
            else:
                if not _isdir(_dir):
                    q.system.fs.createDir(_dir)

            upper = _dir

    def getPageLocation(self, space, page):
        """
        this method returns the absoulte file path of a page
        @params space : string that represents the space name:, example View
        @type   space : string
        @params page  : object page
        @type   page  : object
        """

        crumbs = self._breadcrumbs(page)
        _join = q.system.fs.joinPaths
        _isfile = q.system.fs.isFile
        _isdir = q.system.fs.isDir
        _write = q.system.fs.writeFile

        _dir = self._getDir(space)
        for level in crumbs:
            name = level['name']
            filename = name + ".md"
            _file = _join(_dir, filename)
            _dir = _join(_dir, name)

        return _file

    def _syncPageDelete(self, space, crumbs):
        _join = q.system.fs.joinPaths
        _isfile = q.system.fs.isFile
        _isdir = q.system.fs.isDir

        _dir = self._getDir(space)
        for i, level in enumerate(crumbs):
            name = level['name']
            filename = name + ".md"
            _file = _join(_dir, filename)
            _dir = _join(_dir, name)

            if i == len(crumbs) - 1:
                if _isdir(_dir):
                    q.system.fs.removeDirTree(_dir)
                if _isfile(_file):
                    q.system.fs.removeFile(_file)

    def _deletePage(self, space, page):
        def deleterecursive(guid):
            _filter = self.connection.page.getFilterObject()
            _filter.add('page', "parent", guid, True)

            for chguid in self.connection.page.find(_filter):
                deleterecursive(chguid)

            self.connection.page.delete(guid)

        crumbs = self._breadcrumbs(page)
        deleterecursive(page.guid)
        self._syncPageDelete(space, crumbs)

    def deletePageByGUID(self, guid):
        """
        Deletes a page and its chlidren (recursively).

        @type guid: GUID
        @param guid: Page guid
        """
        page = self.getPageByGUID(guid)
        space = self.getSpace(page.space)
        self._deletePage(space.name, page)

    def deletePage(self, space, name):
        page = self.getPage(space, name)
        self._deletePage(space, page)

    def createSpace(self, name, tagsList=list(), repository="", repo_username="", repo_password="", order=None, createHomePage=True):
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
        description = "%s management page" % name
        self.createPage(ADMINSPACE, spacefile, spacectnt, title=name, parent="Spaces", description=description)

        return space

    def createProject(self, name, path, tagsList=list()):
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
        breadcrumbs = list()
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

    def _createPage(self, space, name, content, title=None, tagsList=list(), category='portal',
                   parent=None, filename=None, contentIsFilePath=False, pagetype="md", description = None, order=None):

        space = self.getSpace(space)
        if self.pageExists(space.guid, name):
            q.errorconditionhandler.raiseError("Page %s already exists."%name)

        page = self.connection.page.new()
        params = {"name":name, "pagetype": pagetype, "space":space.guid, "category":category,
                  "title": title, "filename":filename, "description": description,
                  "content":q.system.fs.fileGetContents(content) if contentIsFilePath else content
                 }
        for key in params:
            if params[key] != None:
                setattr(page, key, params[key])

        page.creationdate = str(time.time())

        try:
            page.order = int(order)
        except: #pylint: disable=W0702
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

    def createPage(self, space, name, content, order=None, title=None, tagsList=list(), category='portal',
                   parent=None, filename=None, contentIsFilePath=False, pagetype="md", description = None):
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

        # HACK to prevent race conditions causing creation of pages with the same name in DB:
        lock = '%s_%s' % (space, name)
        exceptionText = "The page is already about to be created."
        try:
            locklib.aquire_lock(exceptionText, lock)
        except locklib.isLockedException:
            q.logger.log(exceptionText)
            return

        try:
            space = self.getSpace(space)
            page = self._createPage(space=space, name=name, content=content,
                             order=order, title=title, tagsList=tagsList, category=category,
                             parent=parent, filename=filename, contentIsFilePath=contentIsFilePath,
                             pagetype=pagetype, description = description)

            self._syncPageToDisk(space.name, page)
        finally:
            locklib.release_lock(lock)

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
            description = '%s management page' % newname
            self.updatePage(space = ADMINSPACE, old_name = oldspacefile, name=newspacefile, content=p.core.codemanagement.api.getSpacePage(newname),
                title=newname, description=description)

            #sync file system
            self._moveDir(self._getDir(oldname),
                          self._getDir(newname))

        return space

    def _updatePage(self, space, old_name, name=None, tagsList=None, content=None, description = None,
                   order=None, title=None, parent=None, category=None, pagetype=None, filename=None, contentIsFilePath=False):

        space = self.getSpace(space)
        page = self.getPage(space.guid, old_name)

        params = {"name": name, "pagetype": pagetype, "category":category,
                  "title": title, "order": order, "filename":filename, "description": description,
                  "content":q.system.fs.fileGetContents(content) if contentIsFilePath else content
                  }

        for key in params:
            if params[key] != None:
                setattr(page, key, params[key])
        page.creationdate = str(time.time())

        if tagsList:
            page.tags = ' '.join(tagsList)

        if parent:
            parent_page = self.getPage(space, parent)
            page.parent = parent_page.guid

        self.connection.page.save(page)

        return page

    def updatePage(self, space, old_name, name=None, tagsList=None, content=None,
                   order=None, title=None, parent=None, category=None, pagetype=None, filename=None, contentIsFilePath=False, description=None):
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

        # HACK to prevent race conditions causing creation of pages with the same name in DB:
        lock = '%s_%s' % (space, old_name)
        exceptionText = "The page is already about to be updated."
        try:
            locklib.aquire_lock(exceptionText, lock)
        except locklib.isLockedException:
            q.logger.log(exceptionText)
            return

        try:
            space = self.getSpace(space)
            if parent:
                oldPageObject = self.getPage(space.guid, old_name) #this we need if we change parent
            else:
                oldPageObject = None

            page = self._updatePage(space=space, old_name=old_name, name=name, tagsList=tagsList, content=content,
                             order=order, title=title, parent=parent, category=category,
                             pagetype=pagetype, filename=filename, contentIsFilePath=contentIsFilePath, description=description)
            self._syncPageToDisk(space.name, page, old_name, oldPageObject)
        finally:
            locklib.release_lock(lock)
        return page

    def findMacroConfig(self, space="", page="", macro="", configId=None, username=None, exact_properties=None):
        configFilter = self.connection.config.getFilterObject()
        exact_properties = exact_properties or ()
        if space:
            space = self._getSpaceGuid(space)
            configFilter.add('config', 'space', space, 'space' in exact_properties)
            if page:
                configFilter.add('config', 'page', self._getPageInfo(space, page)[0]['guid'],
                    'page' in exact_properties)
        configFilter.add('config', 'macro', macro, 'macro' in exact_properties)
        configFilter.add('config', 'username', username, 'username' in exact_properties)
        if configId:
            configFilter.add('config', 'configid', configId, 'configid' in exact_properties)
        return self.connection.config.findAsView(configFilter, 'config')

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
        import tarfile #pylint: disable=W0404
        def filterFiler(filename):
            return (filename.startswith("/") or filename.startswith(".."))
        join = q.system.fs.joinPaths
        q.logger.log('importing file %s for space %s' % (filename, space), 5)
        tarFile = tarfile.open(filename)
        invalidlinks = filter(filterFiler, tarFile.getnames()) #pylint: disable=W0141
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
        import tarfile #pylint: disable=W0404
        join = q.system.fs.joinPaths
        def buildTree(client, path, space, pagenams = None):
            if not pagenams:
                pagenams = client.listChildPages(space)
            for pagename in pagenams:
                childpages = client.listChildPages(space, pagename)
                if childpages:
                    pagepath = join(path, pagename)
                    q.system.fs.createDir(pagepath)
                    buildTree(client, pagepath, space, childpages)
                page = client.getPage(space, pagename)
                filename = join(path, pagename + ".md")
                fpage = open(filename, "a")
                fpage.truncate(0)

                if page.tags:
                    fpage.write("@metadata tagstring = %s\n" % str(page.tags))

                for metadataItem in ('order', 'title', 'description'):
                    metadata = getattr(page, metadataItem)
                    if metadata:
                        fpage.write('@metadata %s = %s\n' % (metadataItem, metadata))

                fpage.write(page.content)
                fpage.close()

        q.logger.log('exporting space %s to file %s' % (space, filename), 5)
        tempdir = join(q.dirs.tmpDir, space)
        q.system.fs.createDir(tempdir)
        buildTree(self, tempdir, space)
        tarFile = tarfile.open(filename, mode="w|gz")
        tarFile.add(tempdir, "")
        tarFile.close()
        q.system.fs.removeDirTree(tempdir)

    def exportPage(self, space, filename, spacesRoot = None):
        """
        this method writes the page on the disk, with metadata and regular content
        @params space: string to represent the space name
        @type space: string
        @params filename: string to represent the file name
        @type filename: string
        @params spacesRoot: string to help construct the folder path(together with the path of file relative to the parent of the space)
                            where to write the file, if None overwrite existing file
                            example: space = 'View', filename='florin', spacesRoot = 'root', the final destination will be: /root/View/florin.md
        @type spacesRoot: string
        """

        spaceobject = self.getSpace(space)
        spaceguid = spaceobject.guid
        page_info = self.pageFind(name = filename, space = spaceguid, exact_properties=("name", "space"))
        if len(page_info) > 1:
            raise ValueError('Multiple pages found!')

        pageObject = self.getPage(space, filename)
        filePath = self.getPageLocation(space, pageObject)
        if spacesRoot:
            filePath = os.path.relpath(filePath, os.path.dirname(self._getDir(space)))
            filePath = os.path.join(spacesRoot, filePath)
        q.system.fs.createDir(os.path.dirname(filePath))

        #we write the metadata, and also the content of the page
        metadataDict = {}
        head = '@metadata'
        metadataDict['title']       = '%s title=%s\n' % (head, pageObject.title) if pageObject.title != None else ""
        metadataDict['description'] = '%s description=%s\n' % (head, pageObject.description) if pageObject.description != None else ""
        metadataDict['tagstring']   = '%s tagstring=%s\n' % (head, pageObject.tags) if pageObject.tags != None else ""
        metadataDict['order']       = '%s order=%s\n' % (head, pageObject.order) if pageObject.order != None else ""
        pageContent = pageObject.content if pageObject.content != None else ""

        finalContent = str()
        for metadata in metadataDict:
            finalContent = '%s%s' % (finalContent, metadataDict[metadata])
        finalContent = '%s\n%s' % (finalContent, pageContent)

        q.system.fs.writeFile(filePath, finalContent)


    def hgCheckInfo(self, space, repository, repo_username, repo_password):
        if space.repository.url != repository or space.repository.username != repo_username or \
            (repo_password and space.repository.password != repo_password):

            self.updateSpace(space.guid, repository=repository, repo_username=repo_username,
                repo_password=repo_password)
            return True
        return False

    def createRepoUrl(self, repo):
        from urlparse import urlsplit, urlunsplit #pylint: disable=W0404
        url = urlsplit(repo.url)
        return urlunsplit((url.scheme, "%s:%s@%s" % (repo.username, repo.password, url.netloc), url.path, url.query, url.fragment)) #pylint: disable=E1103

    def hgPushSpace(self, space, repository, repo_username, repo_password=None):
        if not repository:
            return "Please give a repository to push to."
        join = q.system.fs.joinPaths
        tempdir = join(q.dirs.tmpDir, space) #here we clone the repo
        spaceInfo = self.getSpace(space)

        #check if we need to update the repo in osis
        if self.hgCheckInfo(spaceInfo, repository, repo_username, repo_password):
            #update to reflect changes
            spaceInfo = self.getSpace(space)

        repoUrl = self.createRepoUrl(spaceInfo.repository)

        q.logger.log('pushing space %s to %s' % (spaceInfo.name, spaceInfo.repository.url), 5)

        #we clone the repo
        hg = q.clients.mercurial.getclient(tempdir, repoUrl)
        #we copy the space in the same dir as where we cloned the repo
        spaceDir = self._getDir(space)
        q.system.fs.copyDirTree(spaceDir, tempdir)

        #check if we already have the latest version
        retval, msg = hg._hgCmdExecutor("incoming", source=hg.getUrl(), die=False, autoCheckFix=False) #pylint: disable=W0212
        if retval == 1 and "no changes found" in msg: #no changes we can push
            #set the username for the commit
            hg._ui.environ["HGUSER"] = spaceInfo.repository.username #pylint: disable=W0212
            hg.addremove('Add new files, and drop deleted files')
            hg.pushcommit("automated commit by Alkira", addRemoveUntrackedFiles=True)
            q.system.fs.removeDirTree(tempdir)
            return True
        else:
            q.system.fs.removeDirTree(tempdir)
            return False

    def hgPullSpace(self, space, repository, repo_username, repo_password=None, dontSync=False):
        if not repository:
            return "Please give a repository to pull from."

        join = q.system.fs.joinPaths
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
        q.system.fs.removeDirTree(join(repoDir, '.hg'))
        #resync pages for space
        if not dontSync:
            self.syncPortal(space=spaceInfo.name)

        return True

    def getitems(self, prop, space=None, term=None):
        page = self.osis.findTable("ui", "page")

        space = self.getSpace(space)

        t = term.split(', ')[-1] if term else ''

        columns = [ getattr(page.c, prop) ]
        where = []

        where.append(page.c.space == space.guid)

        if t:
            where.append(getattr(page.c, prop).like('%%%s%%' % t))

        select = sqlalchemy.select(columns, whereclause=sqlalchemy.and_(*where), distinct=True)

        qr = self.osis.runSqlAlchemyQuery(select)
        result = []
        for row in qr:
            result.append(row[0])

        return result

    def syncPortal(self, path=None, space=None, page=None, cleanup=None):
        def deletePages(space):
            pages = self.pageFind(space=space)
            for page in pages:
                self.connection.page.delete(page)

        def pageDuplicate(page):
            page_name = q.system.fs.getBaseName(page)
            if page_name in page_occured:
                q.errorconditionhandler.raiseError("Another page with the name '%s' already exists on this space. Will NOT create/update the following page (%s)"% (page_name, page))
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

            #if the page get's updated, then leave the metadata to be the one from the disk or to be None values, so that the values from the database are preserved
            if len(page_info) == 1:
                title = page_content_dict.get('title')
                order = page_content_dict.get('order')
                order = int(order) if order else None
                description = page_content_dict.get('description')
                tags = page_content_dict.get('tagstring')
                if tags:
                    tags = tags.split(" ")
                    tags = set(tags)
                    keys = list()
                    for tag in tags:
                        if tag.find(':') != -1:
                            keys.append(tag.split(':')[0])

                    if 'space' not in keys:
                        tags.add('space:%s' % space)

                    if 'page' not in keys:
                        tags.add('page:%s' % name)

                    for tag in re.sub('((?=[A-Z][a-z])|(?<=[a-z])(?=[A-Z]))', ' ', name).strip().split(' '):
                        tags.add(tag)

            else:
                title = page_content_dict.get('title', name)
                order = int(page_content_dict.get('order', '10000'))
                description = page_content_dict.get('description')
                # Creating and setting tags
                tags = page_content_dict.get('tagstring', "").split(" ")
                tags = set(tags)
                tags.add('space:%s' % space)
                tags.add('page:%s' % name)
                for tag in re.sub('((?=[A-Z][a-z])|(?<=[a-z])(?=[A-Z]))', ' ', name).strip().split(' '):
                    tags.add(tag)

            if name == "Home" and spaceobject.name != "Admin":
                self.updateSpace(spaceobject.name, order=int(page_content_dict.get('spaceorder', '1000')))

            save_page(space=space, name=name, content=content, order=order, title=title, tagsList=tags, category='portal', parent=parent, description = description)

        def alkiraTree(folder_paths, root_parent=None): #pylint: disable=W0613
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
        portal_spaces = sorted(portal_spaces, lambda x, y: -1 if x.endswith("/" + ADMINSPACE) else 1)

        for folder in portal_spaces:
            space = folder.split(os.sep)[-1]
            spaceguid = None
            if space not in self.listSpaces():
                #create space
                self.createSpace(space, createHomePage=False)

            spaceobject = self.getSpace(space)
            spaceguid = spaceobject.guid

            q.console.echo('Syncing space: %s' % space)

            page_occured = list()

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
            searchfilter.add('user', 'login', login, True)
        user = self.connection.user.findAsView(searchfilter, 'user')
        return user

    def listUsers(self, login=None):
        return map(lambda item: item["login"], self.listUserInfo(login)) #pylint: disable=W0141

    def listUserInfo(self, login=None):
        return self._getUserInfo(login)

    def listUsersInfo(self):
        usersInfo = list()
        users = self._getUserInfo()
        for user in users:
            usersInfo.append({"name": user["name"], "guid": user["guid"],
                "groups": filter(None, user["groupguids"].split(";"))}) #pylint: disable=W0141
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
        searchfilter.add('user', 'login', name, True)
        user = self.connection.user.findAsView(searchfilter, 'user')
        if user and len(user) == 1:
            return filter(None, user[0]["groupguids"].split(";")) #pylint: disable=W0141

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
            searchfilter.add('group', 'name', name, True)
        group = self.connection.group.findAsView(searchfilter, 'group')
        return group

    def deleteGroup(self, groupguid, oauthInfo=None):
        return self._callAuthService("deleteUsergroup", oauthInfo, usergroupid=groupguid)

    def updateGroup(self, groupguid, name):
        group = self.connection.group.get(groupguid)
        group.name = name
        self.connection.group.save(group)
        return group.guid

    def listGroupsInfo(self):
        groupsInfo = list()
        groups = self._getGroupInfo()
        for group in groups:
            groupsInfo.append({"name": group["name"], "guid": group["guid"]})
        return groupsInfo

    def listGroups(self, name):
        return map(lambda item: item["name"], self._getGroupInfo(name)) #pylint: disable=W0141

    def assignRule(self, groupguids, function, context, oauthInfo=None):
        return self._callAuthService("authorise", oauthInfo, groups=groupguids, functionname=function, context=context)

    def _getRuleInfo(self, groupguid=None, function=None, context=None):
        searchfilter = self.connection.authoriserule.getFilterObject()
        if groupguid:
            searchfilter.add('authoriserule', 'groupguids', ";" + groupguid + ";", False)
        if function:
            searchfilter.add('authoriserule', 'function', function, True)
        if context:
            searchfilter.add('authoriserule', 'context', context, True)
        rule = self.connection.authoriserule.findAsView(searchfilter, 'authoriserule')
        return rule

    def revokeRule(self, groupguids, function, context, oauthInfo=None):
        return self._callAuthService("unAuthorise", oauthInfo, groups=groupguids, functionname=function,
            context=context)

    def listRulesInfo(self):
        rulesInfo = list()
        rules = self._getRuleInfo()
        for rule in rules:
            rulesInfo.append({"name": rule["guid"], "guid": rule["guid"],
                "groups": filter(None, rule["groupguids"].split(";")),  #pylint: disable=W0141
                "function": rule["function"], "context": rule["context"]})
        return rulesInfo

    def createDefaultRules(self):
        try:
            adminGuid = self.createUser("admin", "Admin User", "admin")
        except: #pylint: disable=W0702
            return

        import sys #pylint: disable=W0404
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
            except: #pylint: disable=W0702
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


        from lfw import LFWService #pylint: disable=F0401
        assignRules(LFWService.getAuthorizedFunctions())

        assignRules(AuthService.getAuthorizedFunctions())

        from ide import ide #pylint: disable=F0401
        assignRules(ide.getAuthorizedFunctions())

    def createBookmark(self, name, url, order=99):
        bookmark = self.connection.bookmark.new()
        bookmark.name = name
        bookmark.url = url
        bookmark.order = order
        self.connection.bookmark.save(bookmark)
        return bookmark

    def updateBookmark(self, bookmarkguid, name=None, url=None, order=None):
        if not any((name, url, order)):
            return

        bookmark = self.connection.bookmark.get(bookmarkguid)
        if name:
            bookmark.name = name
        if url:
            bookmark.url = url
        if order != None:
            bookmark.order = order

        self.connection.bookmark.save(bookmark)
        return bookmark

    def deleteBookmark(self, bookmarkguid):
        self.connection.bookmark.delete(bookmarkguid)

    def listBookmarks(self):
        _filter = self.connection.bookmark.getFilterObject()
        bookmarks = self.connection.bookmark.findAsView(_filter, 'bookmark')

        def byOrder(x, y):
            return cmp(x["order"], y["order"])

        bookmarks.sort(byOrder)
        return bookmarks
