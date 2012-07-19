__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'authoriserule'
    domain = "ui"
    appname = params['appname']
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, rootobject):
        view = connection.viewCreate(domain, rootobject, rootobject)
        view.setCol('groupguids', q.enumerators.OsisType.STRING, True, index=True)
        view.setCol('function', q.enumerators.OsisType.STRING, True, index=True)
        view.setCol('context', q.enumerators.OsisType.STRING, True, index=True)
        connection.viewAdd(view)
