from alkira.lfw import LFWService
from alkira.alkira import Alkira

class PagesManager(object):
    '''
    Alkira related pages operations manager
    '''
    
    def __init__(self):
        self._lfw = LFWService()
        self._alkira = Alkira()

    def createPage(self, service, space, name, content, parent=None, order=None, title=None, tags="", category='portal', pagetype="md"):
        '''
        Create a new page into Alkira into the specified space
        
        @param service:  The service to which this extension belongs
        @type service:   Application Server Service
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
        self._lfw.createPage(service, space=space, name=name, content=content, parent=parent, order=order, title=title,
                             tags=tags, category=category, pagetype=pagetype)

    def getPage(self, service, space, name):
        '''
        Retrieve page from Alkira
        
        @param service: The service with which this library is used
        @type service:  Application Server service
        @param space:   Alkira space name
        @type space:    string
        @param name:    Alkira page name
        @type name:     string
        '''
        return self._lfw.getPage(service, space, name)
