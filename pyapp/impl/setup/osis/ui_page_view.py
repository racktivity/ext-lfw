__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'page'
    domain = "ui"
    appname = params['appname']
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, rootobject):
        view = connection.viewCreate(domain, rootobject, rootobject)
        view.setCol('name', q.enumerators.OsisType.STRING, True, index=True)
        view.setCol('space', q.enumerators.OsisType.UUID, True, index=True)
        view.setCol('category', q.enumerators.OsisType.STRING, True, index=True)
        view.setCol('parent', q.enumerators.OsisType.UUID, True, index=True)
        view.setCol('tags', q.enumerators.OsisType.STRING, True, index=True)
        view.setCol('order', q.enumerators.OsisType.INTEGER, True)
        view.setCol('title', q.enumerators.OsisType.STRING, True)
        view.setCol('pagetype', q.enumerators.OsisType.STRING, True)
        connection.viewAdd(view)
