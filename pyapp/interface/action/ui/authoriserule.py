class authoriserule:
    """
    Authoriserule object actions
    """

    def create(self, groupguids, function, context, jobguid="", executionparams=None):
        """
        Create a new authoriserule object.

        @param groupguids:       list of the group
        @type groupguids:        list of guids

        @param function:         name of the function the authorise rule is about
        @type function:          string

        @param context:          context of the authorise rule
        @type context:           dict of strings

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with autoriserule object guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        """

    def find(self, groupguid="", function="", context="", jobguid="", executionparams=None):
        """
        Returns a list of authoriserule objects which met the find criteria.

        @execution_method = sync
        @security administrators

        @param groupguids:             list of the group
        @type groupguids:              list of guids

        @param function:               name of the function the authorise rule is about
        @type function:                string

        @param context:                context of the authorise rule
        @type context:                 string

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

    def delete(self, authoriseruleguid, jobguid="",executionparams=None):
        """
        Delete the group object with the guid specified.

        @security: administrator
        @execution_method = sync

        @param authoriseruleguid:        guid of the authoriserule object
        @type authoriseruleguid:         guid

        @param jobguid:                  guid of the job if available else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        """

    def update(self, authoriseruleguid, groupguids=list(), function="", context=dict(), executionparams=dict()):
        """
        Update a group object name.

        @param authoriseruleguid:        guid of the authoriserule object
        @type authoriseruleguid:         guid

        @param groupguids:               list of the group
        @type groupguids:                list of guids

        @param function:                 name of the function the authorise rule is about
        @type function:                  string

        @param context:                  context of the authorise rule
        @type context:                   dict of strings

        @param jobguid:                  guid of the job if available else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with user object guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        """
