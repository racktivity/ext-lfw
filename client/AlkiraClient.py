from pylabs import q, p

import os, re

class AlkiraClient:

    def getClient(self, hostname, appname):
        """
        Gets a client object.

        @type hostname: String
        @param hostname: The IP that the Alkira Client will use to get a connection and add the pages.

        @return: A client object.
        """
        return Client(hostname, appname)

class Client:

    def __init__(self, hostname, appname):
        api = p.application.getAPI(appname, host=hostname, context=q.enumerators.AppContext.APPSERVER)
        self.connection = api.model.ui

    def _getPageInfo(self, space, name):
        page_filter = self.connection.page.getFilterObject()
        page_filter.add('ui_view_page_list', 'name', name, True)
        page_filter.add('ui_view_page_list', 'space', space, True)
        page_info = self.connection.page.findAsView(page_filter, 'ui_view_page_list')
        return page_info

    def _getParentGUIDS(self, guid_list):
        parent_list = []
        for guid in guid_list:
            page = self.connection.page.get(guid)
            if page.parent:
                parent_list.append(page.parent)

        return parent_list

    def listPages(self, space):
        """
        Lists all the pages in a certain space.

        @type space: String
        @param space: The name of the space.
        """
        PAGES = 'SELECT ui_page.ui_view_page_list."name" FROM ui_page.ui_view_page_list WHERE ui_page.ui_view_page_list.space = \'%s\'' %space
        query = self.connection.page.query(PAGES)
        return map(lambda item: item["name"], query)

    def listSpaces(self):
        """
        Lists all the spaces.
        """
        SPACES = 'SELECT DISTINCT ui_page.ui_view_page_list."space" FROM ui_page.ui_view_page_list'
        query = self.connection.page.query(SPACES)
        return map(lambda item: item["space"], query)

    def listPageInfo(self, space):
        """
        Lists all the pages in a space with their info.

        @type space: String
        @param space: The name of the space.
        """
        page_info = 'SELECT ui_page.ui_view_page_list."name", ui_page.ui_view_page_list."guid", ui_page.ui_view_page_list."parent", ui_page.ui_view_page_list."title", ui_page.ui_view_page_list."order" FROM ui_page.ui_view_page_list WHERE ui_page.ui_view_page_list.space = \'%s\'' %space
        query = self.connection.page.query(page_info)
        return query

    def pageExists(self, space, name):
        """
        Checks whether a page exists or not.

        @type space: String
        @param space: The name of the space.

        @type name: String
        @param name: The name of the page.

        @return: True if the page exists, False otherwise.
        """
        if self._getPageInfo(space, name):
            return True
        else:
            return False        

    def getPage(self, space, name):
        """
        Gets a page object.

        @type space: String
        @param space: The name of the space.

        @type name: String
        @param name: The name of the page.

        @return: Page object.
        """
        if not self.pageExists(space, name):
            q.errorconditionhandler.raiseError("Page %s does not exist."%name)
        else:
            page_info = self._getPageInfo(space, name)
            page = self.connection.page.get(page_info[0]['guid'])
            return page
    
    def deleteSpace(self, space=None):
        if space is None:
            spaces = self.listSpaces()
        else:
            spaces = [space]
            
        for s in spaces:
            pages = self.listPages(s)
            for page in pages:
                self.deletePage(s, page)
                
        
    def deletePage(self, space, name):
        """
        Deletes a page.

        @type space: String
        @param space: The name of the space.

        @type name: String
        @param name: The name of the page.
        """
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
        page = self.getPage(old_space, old_name)

        if space:
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
        
