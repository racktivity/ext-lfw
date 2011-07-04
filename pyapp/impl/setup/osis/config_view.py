__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'config'
    domain = "ui"
    appname = params['appname']
    view_name = '%s_view_%s_list' % (domain, rootobject)
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('space', q.enumerators.OsisType.UUID, True)
        view.setCol('page', q.enumerators.OsisType.UUID, True)
        view.setCol('macro', q.enumerators.OsisType.STRING, True)
        view.setCol('configid', q.enumerators.OsisType.STRING, True)
        connection.viewAdd(view)

        indexes = ['space', 'page', 'macro', 'configid']
        for field in indexes:
            context = {'schema': "%s_%s" % (domain, rootobject), 'view': view_name, 'field': field}
            connection.runQuery("CREATE INDEX %(field)s_%(schema)s_%(view)s ON %(schema)s.%(view)s (%(field)s)" % context)
