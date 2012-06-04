__author__ = 'Racktivity'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB
from osis.store import OsisConnection

def main(q, i, params, tags):
    rootobject = 'bookmark'
    domain = "ui"
    appname = params['appname']
    scheme_name = OsisConnection.getSchemeName(domain = domain, objType = rootobject)
    view_name = OsisConnection.getTableName(domain = domain, objType = rootobject)
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('name', q.enumerators.OsisType.STRING, False)
        view.setCol('url', q.enumerators.OsisType.STRING, False)
        view.setCol('order', q.enumerators.OsisType.INTEGER, False)
        connection.viewAdd(view)

        context = {'schema': scheme_name, 'view': view_name, 'field': 'name'}
        connection.runQuery("CREATE INDEX %(view)s_%(field)s ON %(schema)s.%(view)s (%(field)s)" % context)
