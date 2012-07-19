__author__ = 'Racktivity'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'bookmark'
    domain = "ui"
    appname = params['appname']
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, rootobject):
        view = connection.viewCreate(domain, rootobject, rootobject)
        view.setCol('name', q.enumerators.OsisType.STRING, False, index=True)
        view.setCol('url', q.enumerators.OsisType.STRING, False)
        view.setCol('order', q.enumerators.OsisType.INTEGER, False)
        connection.viewAdd(view)
