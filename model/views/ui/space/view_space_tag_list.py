__tags__ = 'setup'

from osis.store.OsisDB import OsisDB

def main(q, i, p, params, tags):

    domain = 'ui'
    rootobject = 'space'
    viewname = 'view_space_tag_list'
    
    connection = OsisDB().getConnection('main')
    
    if not connection.viewExists(domain, rootobject, viewname):
        view = connection.viewCreate(domain, rootobject, viewname)
        view.setCol('tag', q.enumerators.OsisType.STRING, False)
        connection.viewAdd(view)
    
        indexes = ['tag']
        for field in indexes:
            connection.runQuery("CREATE INDEX %(field)s_%(schema)s_%(view)s ON %(schema)s.%(view)s (%(field)s)"%{'schema': '%s_%s' % (domain, rootobject), 
                                                                                                                 'view': '%s_%s' % (domain, viewname) , 
                                                                                                                 'field':field})
