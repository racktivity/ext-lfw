class AlkiraCommon(object):
    '''
    Alkira common operations
    '''

    def __init__(self):
        self._separator = ':'

    def getPageId(self, space, name):
        '''
        Retrieve the id of a persistent Alkira page
        
        @param space: Alkira space
        @type space:  string
        @param name:  Alkira page name
        @type name:   string
        '''
        if not space or not name:
            raise ValueError('Invalid space or name values. Space: %s, Name: %s' % (space, name))
        
        return '%s%s%s' % (space, self._separator, name)
