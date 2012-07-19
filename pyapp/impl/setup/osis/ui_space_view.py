__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'space'
    domain = "ui"
    appname = params['appname']
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, rootobject):
        view = connection.viewCreate(domain, rootobject, rootobject)
        view.setCol('name', q.enumerators.OsisType.STRING, True, index=True, unique=True)
        view.setCol('tags', q.enumerators.OsisType.STRING, True, index=True)
        view.setCol('repository', q.enumerators.OsisType.STRING, True, index=True)
        view.setCol('repo_username', q.enumerators.OsisType.STRING, True)
        view.setCol('order', q.enumerators.OsisType.INTEGER, True)
        connection.viewAdd(view)
