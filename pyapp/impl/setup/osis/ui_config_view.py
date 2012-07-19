__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'config'
    domain = "ui"
    appname = params['appname']
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, rootobject):
        view = connection.viewCreate(domain, rootobject, rootobject)
        view.setCol('space', q.enumerators.OsisType.UUID, True, index=True)
        view.setCol('page', q.enumerators.OsisType.UUID, True, index=True)
        view.setCol('macro', q.enumerators.OsisType.STRING, True, index=True)
        view.setCol('configid', q.enumerators.OsisType.STRING, True, index=True)
        view.setCol('username', q.enumerators.OsisType.STRING, True, index=True)
        connection.viewAdd(view)
