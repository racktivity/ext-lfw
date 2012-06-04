__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB
from osis.store import OsisConnection

def main(q, i, params, tags):
    rootobject = 'page'
    domain = "ui"
    appname = params['appname']
    scheme_name = OsisConnection.getSchemeName(domain = domain, objType = rootobject)
    view_name = OsisConnection.getTableName(domain = domain, objType = rootobject)
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('name', q.enumerators.OsisType.STRING, True)
        view.setCol('space', q.enumerators.OsisType.UUID, True)
        view.setCol('category', q.enumerators.OsisType.STRING, True)
        view.setCol('parent', q.enumerators.OsisType.UUID, True)
        view.setCol('tags', q.enumerators.OsisType.STRING, True)
        view.setCol('order', q.enumerators.OsisType.INTEGER, True)
        view.setCol('title', q.enumerators.OsisType.STRING, True)
        view.setCol('pagetype', q.enumerators.OsisType.STRING, True)
        connection.viewAdd(view)

        indexes = ['name', 'space', 'category', 'parent', 'tags']
        for field in indexes:
            context = {'schema': scheme_name, 'view': view_name, 'field': field}
            connection.runQuery("CREATE INDEX %(view)s_%(field)s ON %(schema)s.%(view)s (%(field)s)" % context)
