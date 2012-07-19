class bookmark:
    """
    bookmark object actions
    """
    def __init__(self):
        pass

    def create(self, name, url, order=99, jobguid="", executionparams=None):
        """
        Create a new bookmark object.

        @authorize =

        @param name:             name of the bookmark
        @type name:              string

        @param url:              url the bookmark points to
        @type url:               string

        @param order:            order of the boomark
        @type order:             integer

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with POP configuration object guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        """

    def find(self, name="", exact_properties=None, jobguid="", executionparams=None):
        """
        Returns a list of bookmark objects which met the find criteria.

        @authorize =

        @execution_method = sync
        @security administrators

        @param name:                   name of the bookmark
        @type name:                    string

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

    def getObject(self, rootobjectguid, jobguid="", executionparams=None):
        """
        Gets the rootobject.

        @authorize =

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

    def delete(self, bookmarkguid, jobguid="", executionparams=None):
        """
        Delete the bookmark object with the guid specified.

        @authorize =

        @security: administrator

        @execution_method = sync

        @param bookmarkguid:             guid of the bookmark object
        @type bookmarkguid:              guid

        @param jobguid:                  guid of the job if available else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        """

    def update(self, bookmarkguid, name=None, url=None, order=None, jobguid="", executionparams=dict()):
        """
        Update a bookmark object.

        @authorize =

        @param bookmarkguid:     guid of the bookmark object
        @type bookmarkguid:      guid

        @param name:             name of the bookmark
        @type name:              string

        @param url:              url the bookmark points to
        @type url:               string

        @param order:            order of the boomark
        @type order:             integer

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with POP configuration object guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        """
