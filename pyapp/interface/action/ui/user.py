class user:
    """
    User object actions
    """

    def create(self, login, name=None, password=None, jobguid="", executionparams=None):
        """
        Create a new user object.

        @authorize =

        @param login:            login of the user
        @type login:             string

        @param name:             name of the user
        @type name:              string

        @param password:         password of the user
        @type password:          string

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with user object guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        """

    def find(self, login="", name="", exact_properties=None, jobguid="", executionparams=None):
        """
        Returns a list of user objects which met the find criteria.

        @execution_method = sync
        @security administrators
        @authorize =

        @param login:                  login of the user
        @type login:                   string

        @param name:                   name of the user
        @type name:                    string

        @param exact_properties:       a list containing the names of parameters for which we search for an exact match
        @type exact_properties:        list

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
        @authorize =

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
        @authorize =

        @param userguid:                 guid of the user object
        @type userguid:                  guid

        @param jobguid:                  guid of the job if available else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        """

    def update(self, userguid, name="", password=None, jobguid="", executionparams=dict()):
        """
        Update a user object name.

        @authorize =

        @param userguid:         guid of the user object
        @type userguid:          guid

        @param name:             name of the user
        @type name:              string

        @param password:         password of the user
        @type password:          string

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with user object guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        """

    def addGroup(self, userguid, groupguid, jobguid="", executionparams=None):
        """
        Add a user to a group.

        @authorize =

        @param userguid:         guid of the user object
        @type userguid:          guid

        @param groupguid:        guid of the group to add
        @type groupguid:         guid

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        """

    def deleteGroup(self, userguid, groupguid, jobguid="", executionparams=None):
        """
        Delete a user from a group.

        @authorize =

        @param userguid:         guid of the user object
        @type userguid:          guid

        @param groupguid:        guid of the group to remove
        @type groupguid:         guid

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        """
