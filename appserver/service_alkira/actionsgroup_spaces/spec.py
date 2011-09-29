class Spaces:
    def get(self, name):
        '''
        Get space

        @param name: name of the space
        @type name: string
        '''

    def list(self, term=None):
        '''
        List spaces

        @param term: @todo fill in
        @type term: object
        '''

    def create(self, name, tags=None):
        '''
        Create a new page into Alkira into the specified space

        @param name: Alkira space name
        @type name: string
        @param tags: tags
        @type tags: string
        '''

    def update(self, name, newName, tags=None):
        '''
        Update the name of a space

        @param name: current Alkira space name
        @type name: string
        @param newName: new Alkira space name
        @type newName: string
        @param tags: tags
        @type tags: string
        '''

    def delete(self, name):
        '''
        Delete the space with the argument name

        @param name: current Alkira space name
        @type name: string
        '''

