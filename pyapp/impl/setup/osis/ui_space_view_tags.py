__tags__ = 'setup'

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    domain = 'ui'
    rootobject = 'space'
    conName = params['appname']
    connection = OsisDB().getConnection(conName)
    view_name = '%s_tag_list' % rootobject
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('tag', q.enumerators.OsisType.STRING, False, index=True)
        connection.viewAdd(view)
