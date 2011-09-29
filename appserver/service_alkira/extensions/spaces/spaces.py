from alkira.lfw import LFWService

class SpacesManager(object):
    '''
    Alkira related space operations manager
    '''

    def __init__(self):
        self._lfw = LFWService()

    def get(self, service, name):
        """
        Get the page with the argument name

        @param service: The service to which this extension belongs
        @type service: Application Server Service
        @param name: name of the space
        @type name: string
        """
        self._serviceHack(service)
        return self._lfw.getSpace(name)

    def create(self, service, name):
        '''
        Create a new page into Alkira into the specified space

        @param service: The service to which this extension belongs
        @type service: Application Server Service
        @param name: Alkira space name
        @type name: string
        '''
        self._serviceHack(service)
        return self._lfw.createSpace(name=name)

    def list(self, service):
        '''
        List pages in Alkira

        @param service:  The service to which this extension belongs
        @type service:   Application Server Service
        '''
        self._serviceHack(service)
        return self._lfw.listSpaces()

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
        self._serviceHack(service)
        return self._lfw.updateSpace(name, newName, tags=tags)

    def delete(self, service, name):
        """
        Delete the space with the argument name

        @param service: The service to which this extension belongs
        @type service: Application Server Service
        @param name: name of the service
        @type name: string
        """
        self._serviceHack(service)
        return self._lfw.deleteSpace(name)

    def _serviceHack(self, service):
        self._lfw.service = service
        self._lfw._alkira.service = service
