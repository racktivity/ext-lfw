from pymonkey.InitBase import q
from osis.store.OsisDB import OsisDB

rootobject = 'page'
viewname = 'view_page_tag_list'

connection = OsisDB().getConnection('portal')

if not connection.viewExists(rootobject, viewname):
    view = connection.viewCreate(rootobject, viewname)
    view.setCol('tag', q.enumerators.OsisType.STRING, False)
    connection.viewAdd(view)

indexes = ['tag', 'guid']
for field in indexes:
    connection.runQuery("CREATE INDEX %(field)s_%(schema)s_%(view)s ON %(schema)s.%(view)s (%(field)s)"%{'schema':rootobject, 
                                                                                                         'view': viewname , 
                                                                                                         'field':field})
