from pylabs import q, p

import os

ADMINSPACE = "Admin"

class AlkiraClient:

    def getClient(self, hostname, appname):
        """
        Gets a client object.

        @type hostname: String
        @param hostname: The IP that the Alkira Client will use to get a connection and add the pages.

        @return: A client object.
        """
        return Client(hostname=hostname, appname=appname)

    def getClientByApi(self, api):
        """
        Gets a client object.

        @param api: The application API (p.api)

        @return: A client object.
        """
        return Client(api=api)

class Client:

    def __init__(self, hostname=None, appname=None, api=None):
        """
        Initialize a new Alkira Client with the given (hostname, appname) connection
        but if hostname and appname are not given, the given api is used

        @param hostname: The hostname of alikra

        @param appname: The application name

        @param api: The application api if hostname and appname are not passed
        """
        if hostname and appname:
            api = p.application.getAPI(appname, host=hostname, context=q.enumerators.AppContext.APPSERVER)
        elif not api:
            q.errorconditionhandler.raiseError("'api' is not optional if hostname and appname are empty")

        self.connection = api.model.ui

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

    def _getSpaceInfo(self, name):
        filter = self.connection.space.getFilterObject()
        filter.add('ui_view_space_list', 'name', name, True)
        space = self.connection.space.findAsView(filter, 'ui_view_space_list')
        return space

    def _getParentGUIDS(self, guid_list):
        parent_list = []
        for guid in guid_list:
            page = self.connection.page.get(guid)
            if page.parent:
                parent_list.append(page.parent)

        return parent_list

    def listPages(self, space=None):
        """
        Lists all the pages in a certain space.

        @param space: The name, guid or space object of the space.
        """
        return map(lambda i: i['name'],
                   self.listPageInfo(space))

    def listSpaces(self):
        """
        Lists all the spaces.
        """
        return map(lambda item: item["name"],
                   self.listSpaceInfo())

    def listSpaceInfo(self):
        """
        List all spaces info
        """
        spaces = self.connection.space.findAsView(self.connection.space.getFilterObject(),
                                                  'ui_view_space_list')

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

    def getSpace(self, space):
        """
        Gets a space object

        @param name: The space name, or guid
        """

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

    def deleteSpace(self, space):
        """
        Delete space

        @param space: The space name, object or guid to delete

        @note: Deleting a space will delete all the pages in that space.
        """
        if space == ADMINSPACE:
            raise RuntimeError("Invalid space")

        space = self.getSpace(space)

        pages = self.listPageInfo(space)

        for page in pages:
            self.connection.page.delete(page['guid'])

        self.connection.space.delete(space.guid)
        self.deletePage(ADMINSPACE, space.name)

    def deletePage(self, space, name):
        """
        Deletes a page.

        @type space: String
        @param space: The name of the space.

        @type name: String
        @param name: The name of the page.
        """
        space = self._getSpaceGuid(space)
        page = self.getPage(space, name)
        self.connection.page.delete(page.guid)

    def deletePageAndChildren(self, space, name):
        """
        Deletes a page and its chlidren (recursively).

        @type space: String
        @param space: The name of the space.

        @type name: String
        @param name: The name of the page.
        """
        space = self._getSpaceGuid(space)

        space_filter = self.connection.page.getFilterObject()
        space_filter.add('ui_view_page_list', 'space', space, True)
        space_guids = self.connection.page.find(space_filter)

        delete_list = []
        parent_list = self._getParentGUIDS(space_guids)

        page = self.getPage(space, name)
        delete_list.append(page.guid)
        space_guids.remove(page.guid)

        while (set(delete_list) & set(parent_list)):
            for guid in space_guids:
                page = self.connection.page.get(guid)
                parent_guid = page.parent
                if parent_guid in delete_list:
                    delete_list.append(guid)
                    space_guids.remove(guid)
            parent_list = self._getParentGUIDS(space_guids)

        for page_guid in delete_list:
            self.connection.page.delete(page_guid)

    def createSpace(self, name, tagslist=[], repository="", repo_username="", repo_password=""):
        if self.spaceExists(name):
            q.errorconditionhandler.raiseError("Space %s already exists." % name)

        space = self.connection.space.new()
        space.name = name
        space.tags = ' '.join(tagslist)

        repo = space.repository.new()
        repo.url = repository
        repo.username = repo_username
        repo.password = repo_password
        space.repository = repo

        self.connection.space.save(space)

        if name == ADMINSPACE:
            return

        #create a space page under the default admin space
        spacectnt = p.core.codemanagement.api.getSpacePage(name)
        self.createPage(ADMINSPACE, name, spacectnt, title=name, parent="Spaces")

    def createPage(self, space, name, content, order=None, title=None, tagsList=[], category='portal', parent=None, contentIsFilePath=False):
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
        """
        space = self._getSpaceGuid(space)
        if self.pageExists(space, name):
            q.errorconditionhandler.raiseError("Page %s already exists."%name)
        else:
            page = self.connection.page.new()
            page.space = space
            page.name = name
            page.category = category

            if title:
                page.title = title
            else:
                page.title = name

            if order:
                page.order = order
            else:
                page.order = 10000

            if contentIsFilePath:
                content = q.system.fs.fileGetContents(content)

            page.content = content

            tags = set(tagsList)
            tags.add('space:%s' % space)
            tags.add('page:%s' % name)
            page.tags = ' '.join(tags)

            if parent:
                parent_page = self.getPage(space, parent)
                page.parent = parent_page.guid

            self.connection.page.save(page)

    def updateSpace(self, space, newname=None, tagslist=None, repository=None, repo_username=None, repo_password=None):
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

        self.connection.space.save(space)

        if oldname != newname:
            #rename space page.
            self.updatePage(ADMINSPACE, oldname, name=newname)
        
    def updatePage(self, old_space, old_name, space=None, name=None, tagsList=None, content=None, order=None, title=None, parent=None, category=None, contentIsFilePath=False):
        """
        Updates an existing page.

        @type old_space: String
        @param old_space: The name of the space.

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
        """
        old_space = self._getSpaceGuid(old_space)

        page = self.getPage(old_space, old_name)

        if space:
            space = self._getSpaceGuid(space)
            page.space = space

        if name:
            page.name = name

        if tagsList:
            tags = page.tags.split(' ')
            for tag in tagsList:
                tags.append(tag)

            page_tags = ' '.join(tags)
            page.tags = page_tags

        if content:
            if contentIsFilePath:
                content = q.system.fs.fileGetContents(content)
            page.content = content

        if order:
            page.order = order

        if title:
            page.title = title

        if parent:
            parent_page = self.getPage(old_space, parent)
            page.parent = parent_page.guid

        if category:
            page.category = category

        self.connection.page.save(page)

