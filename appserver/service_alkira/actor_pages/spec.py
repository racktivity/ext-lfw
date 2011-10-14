class pages():
    def createPage(self, space, name, content, parent=None, order=None, title=None, tags="", category='portal',
                   pagetype="md"):
        '''
        Create a new page into Alkira into the specified space
        
        @param space:    Alkira space
        @type space:     string
        @param name:     Alkira page name
        @type name:      string
        @param content:  Alkira page content
        @type content:   string
        @param parent:   Name of parent page
        @type parent:    string
        @param order:    Order of the page
        @type order:     Integer
        @param title:    Page title
        @type title:     string
        @param tags:     Tags you want to add to the page
        @type tags:      string
        @param category: Page category
        @type category:  string
        @param pagetype: Page type
        @type pagetype:  string
        '''

    def getPage(self, space, name):
        '''
        Retrieve page from Alkira
        
        @param space:   Alkira space name
        @type space:    string
        @param name:    Alkira page name
        @type name:     string
        '''

    def deletePage(self, space, name):
        '''
        Delete a page from Alkira
        
        @param space: Space name
        @type space:  string
        @param name:  Page name
        @type name:   string
        '''

    def countPages(self, space=None):
        '''
        Count pages in Alkira
        
        @param space: Alkira space
        @type sapce:  string
        '''
