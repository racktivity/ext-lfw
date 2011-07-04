class user:
    """
    User object actions
    """

    def create(self, name, password, spaces=[], pages=[], tags="", jobguid="", executionparams=None):
        """
        Create a new user object.

        @param name:             name of the user
        @type name:              string

        @param password:             name of the user
        @type password:              string

        @param spaces:            list of user spaces
        @type spaces:             List

        @param pages:            list of user pages
        @type pages:             List

        @param tags:             tags of the page
        @type tags:              string

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with POP configuration object guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        """

    def find(self, name="", tags="", jobguid="", executionparams=None):
        """
        Returns a list of user objects which met the find criteria.

        @execution_method = sync
        @security administrators

        @param name:                   name of the user
        @type name:                    string

        @param tags:                   tags of the user
        @type tags:                    string

        @param jobguid:                guid of the job if available else empty string
        @type jobguid:                 guid
        
        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
 
        @return:                       A list of guids as result and jobguid: {'result': [], 'jobguid': guid}
        @rtype:                        list
 
        @note:                         Example return value:
        @note:                         {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                          'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
 
 
        @raise e:                      In case an error occurred, exception is raised
        """

    def getObject(self, rootobjectguid, jobguid="",executionparams=None):
        """
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:   guid of the job rootobject
        @type rootobjectguid:    guid

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 rootobject
        @rtype:                  rootobject

        @warning:                Only usable using the python client.
        """
        
    def delete(self, userguid, jobguid="",executionparams=None):
        """
        Delete the user object with the guid specified.
        
        @security: administrator
        
        @execution_method = sync
        
        @param userguid:                 guid of the page object
        @type userguid:                  guid
        
        @param jobguid:                  guid of the job if available else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary
        
        @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        """

    def update(self, userguid, name="", password="", tags="", jobguid="", executionparams=dict()):
        """
        Update a user object name and tags.

        @param userguid:         guid of the user object
        @type userguid:          guid

        @param name:             name of the user
        @type name:              string

        @param password:             password of the user
        @type password:              string

        @param tags:             tags of the user
        @type tags:              string

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with user object guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        """

    def addSpace(self, userguid, space, jobguid="", executionparams=dict()):
        """
        Add a space to the user list of spaces.

        @param userguid:         guid of the user object
        @type userguid:          guid

        @param space:             name of the space
        @type space:              string

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True/False as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        """

    def deleteSpace(self, userguid, space, jobguid="", executionparams=dict()):
        """
        Delete a space from the user list of spaces.

        @param userguid:         guid of the user object
        @type userguid:          guid

        @param space:             name of the space
        @type space:              string

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True/False as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        """

    def addPage(self, userguid, page, jobguid="", executionparams=dict()):
        """
        Add a page to the user list of pages.

        @param userguid:         guid of the user object
        @type userguid:          guid

        @param page:             name of the page
        @type page:              string

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True/False as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        """

    def deletePage(self, userguid, page, jobguid="", executionparams=dict()):
        """
        Delete a page from the user list of spaces.

        @param userguid:         guid of the user object
        @type userguid:          guid

        @param page:             name of the page
        @type page:              string

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True/False as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        """
