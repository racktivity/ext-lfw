__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = '_index'
    domain = "ui"
    appname = params['appname']
    view_name = 'global_index_view'
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('name', q.enumerators.OsisType.STRING, False)
        view.setCol('url', q.enumerators.OsisType.STRING, False)
        view.setCol('content', q.enumerators.OsisType.TEXT, True)
        view.setCol('tags', q.enumerators.OsisType.STRING, True)
        connection.viewAdd(view)

        indexes = ['content', 'tags']
        for field in indexes:
            context = {'schema': "%s_%s" % (domain, rootobject), 'view': view_name, 'field': field}
            connection.runQuery("CREATE INDEX %(field)s_%(schema)s_%(view)s ON %(schema)s.%(view)s USING hash (%(field)s)" % context)
