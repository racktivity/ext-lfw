class AlkiraCommon(object):
    '''
    Alkira common operations
    '''

    def __init__(self):
        self._separator = ':'
        self._pagePrefix = "page"
        self._spacePrefix = "space"

    def getPageId(self, space, name):
        '''
        Retrieve the ID of a persistent Alkira page

        @param space: Alkira space name
        @type space:  string
        @param name:  Alkira page name
        @type name:   string
        '''
        self.checkSpaceName(space)
        self.checkPageName(space)

        return self._separator.join([self._pagePrefix, space, name])

    def getSpaceId(self, name):
        '''
        Retrieve the ID of a persistent Alkira space

        @param name:  Alkira page name
        @type name:   string
        '''
        self.checkSpaceName(name)

        return self._separator.join([self._spacePrefix, name])

    @property
    def spacePrefix(self):
        return self._spacePrefix + self._separator

    @property
    def pagePrefix(self):
        return self._pagePrefix + self._separator

    def checkSpaceName(self, name):
        if not name:
            raise ValueError("Invalid space name '%s'" % name)

    def checkPageName(self, name):
        if not name:
            raise ValueError("Invalid page name '%s'" % name)
