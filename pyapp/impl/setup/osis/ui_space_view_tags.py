__tags__ = 'setup'

from osis.store.OsisDB import OsisDB
from osis.store import OsisConnection

def main(q, i, p, params, tags):

    domain = 'ui'
    rootobject = 'space'
    scheme_name = OsisConnection.getSchemeName(domain = domain, objType = rootobject)
    view_name = '%s_tag_list' % rootobject
    conName = params['appname']
    connection = OsisDB().getConnection(conName)
    
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('tag', q.enumerators.OsisType.STRING, False)
        connection.viewAdd(view)
    
        indexes = ['tag']
        for field in indexes:
            context = {'schema': scheme_name, 'view': view_name, 'field': field}
            connection.runQuery("CREATE INDEX %(view)s_%(field)s ON %(schema)s.%(view)s (%(field)s)" % context)
