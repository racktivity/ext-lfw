from alkira.lfw import LFWService
from alkira.alkira import Alkira

class SpaceManager(object):
    '''
    Alkira related space operations manager
    '''

    def __init__(self):
        self._lfw = LFWService()
        self._alkira = Alkira()

    def create(self, service, name):
        '''
        Create a new page into Alkira into the specified space

        @param service: The service to which this extension belongs
        @type service: Application Server Service
        @param name: Alkira space name
        @type name: string
        '''
        self._lfw.createSpace(service, name=name)

    def list(self, service):
        '''
        List pages in Alkira

        @param service:  The service to which this extension belongs
        @type service:   Application Server Service
        '''
        return self._lfw.listSpaces(service)

    def update(self, service, name, newName, tags=None):
        """
        Update the name of a space

        @param service: The service to which this extension belongs
        @type service: Application Server Service
        @param name: current name of the space
        @type name: string
        @param newName: new name of the space
        @type newName: string
        @param tags: tags
        @type tags: string
        """
        return self._lfw.updateSpace(service, name, newName, tags=tags)

    def delete(self, service, name):
        """
        Delete the space with the argument name

        @param service: The service to which this extension belongs
        @type service: Application Server Service
        @param name: name of the service
        @type name: string
        """
        return self._lfw.deleteSpace(service, name)
