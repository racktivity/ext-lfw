class config:
    """
    Config object actions
    """

    def create(self, space, page, macro, data, configid=None, username=None, jobguid="", executionparams=None):
        """
        Create a new page object.

        @param space:            space of the macro
        @type space:             guid

        @param page:             page of the macro
        @type page:              guid

        @param macro:            macro of the config
        @type macro:             string

        @param data:             the data of the config
        @type data:              string

        @param configid:         id of the macro
        @type configid:          string

        @param username:         username of the macro
        @type username:          string

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with POP configuration object guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        """

    def find(self, space="", page="", macro="", configid="", username="", exact_properties=None, jobguid="", executionparams=None):
        """
        Returns a list of config objects which met the find criteria.

        @execution_method = sync
        @security administrators

        @param space:                  space of the macro
        @type space:                   guid

        @param page:                   page of the macro
        @type page:                    guid

        @param macro:                  macro of the config
        @type macro:                   string

        @param data:                   the data of the config
        @type data:                    string

        @param configid:               id of the macro
        @type configid:                string

        @param username:               username of the macro
        @type username:                string

        @param exact_properties:       an iterable of property names whose values should be matched exactly
        @type exact_properties:        iterable of strings

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

    def delete(self, configguid, jobguid="",executionparams=None):
        """
        Delete the config object with the guid specified.

        @security: administrator

        @execution_method = sync

        @param configguid:               guid of the config object
        @type configguid:                guid

        @param jobguid:                  guid of the job if available else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        """

    def update(self, configguid, data, jobguid="", executionparams=dict()):
        """
        Update a given config object.

        @param configguid:       guid of the config object
        @type configguid:        guid

        @param data:             data of the config
        @type data:              string

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with POP configuration object guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        """
