from pylabs.InitBase import q
from osis.store.OsisDB import OsisDB

domain = 'ui'
rootobject = 'page'
viewname = 'view_page_list'

connection = OsisDB().getConnection('main')

if not connection.viewExists(domain, rootobject, viewname):
    view = connection.viewCreate(domain, rootobject, viewname)
    view.setCol('name', q.enumerators.OsisType.STRING, False)
    view.setCol('space', q.enumerators.OsisType.STRING, True)
    view.setCol('category', q.enumerators.OsisType.STRING, True)
    view.setCol('parent', q.enumerators.OsisType.UUID, True)
    view.setCol('content', q.enumerators.OsisType.TEXT, False)
    connection.viewAdd(view)

    indexes = ['name', 'space', 'category', 'parent']

    for field in indexes:
        connection.runQuery("CREATE INDEX %(field)s_%(schema)s_%(view)s ON %(schema)s.%(view)s (%(field)s)"%{'schema': '%s_%s' % (domain, rootobject), 
                                                                                                             'view': '%s_%s' % (domain, viewname), 
                                                                                                             'field':field})
        
    connection.runQuery("CREATE INDEX %(field)s_%(schema)s_%(view)s ON %(schema)s.%(view)s USING hash (%(field)s)"%{'schema':'%s_%s' % (domain, rootobject), 
                                                                                                             'view': '%s_%s' % (domain, viewname) , 
                                                                                                             'field':'content'})
