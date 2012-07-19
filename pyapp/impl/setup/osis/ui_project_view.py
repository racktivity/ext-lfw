__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'project'
    domain = "ui"
    appname = params['appname']
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, rootobject):
        view = connection.viewCreate(domain, rootobject, rootobject)
        view.setCol('name', q.enumerators.OsisType.STRING, False, index=True, unique=True)
        view.setCol('path', q.enumerators.OsisType.STRING, False)
        view.setCol('tags', q.enumerators.OsisType.STRING, True, index=True)
        connection.viewAdd(view)
