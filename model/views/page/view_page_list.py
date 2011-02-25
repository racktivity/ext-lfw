from pymonkey.InitBase import q
from osis.store.OsisDB import OsisDB

rootobject = 'page'
viewname = 'view_page_list'

connection = OsisDB().getConnection('portal')

if not connection.viewExists(rootobject, viewname):
    view = connection.viewCreate(rootobject, viewname)
    view.setCol('name', q.enumerators.OsisType.STRING, False)
    view.setCol('space', q.enumerators.OsisType.STRING, True)
    view.setCol('category', q.enumerators.OsisType.STRING, True)
    view.setCol('parent', q.enumerators.OsisType.UUID, True)
    view.setCol('content', q.enumerators.OsisType.TEXT, False)
    connection.viewAdd(view)

indexes = ['name', 'space', 'category', 'parent', 'content']

for field in indexes:
    connection.runQuery("CREATE INDEX %(field)s_%(schema)s_%(view)s ON %(schema)s.%(view)s (%(field)s)"%{'schema':rootobject, 
                                                                                                         'view': viewname , 
                                                                                                         'field':field})
