from pymonkey import q
import osis
from osis.client import OsisConnection
from osis.client.xmlrpc import XMLRPCTransport
from osis.model.serializers import ThriftSerializer


# @TODO: use sqlalchemy to construct queries - escape values 
# @TODO: add space to filter criteria

SQL_PAGES = 'SELECT DISTINCT page.view_page_list.%(prop)s FROM page.view_page_list'
SQL_PAGES_FILTER = 'SELECT DISTINCT page.view_page_list.%(prop)s FROM page.view_page_list WHERE page.view_page_list.%(prop)s LIKE \'%(term)s%%\''

SQL_PAGE_TAGS = 'SELECT DISTINCT page.view_page_tag_list.%(prop)s FROM page.view_page_tag_list'
SQL_PAGE_TAGS_FILTER = 'SELECT DISTINCT page.view_page_tag_list.%(prop)s FROM page.view_page_tag_list WHERE page.view_page_tag_list.%(prop)s LIKE \'%(term)s%%\''


class LFWService(object):

    def __init__(self):
        
        # Initialize osis
        osis.init('/opt/qbase3/libexec/osis')
        transport = XMLRPCTransport('http://127.0.0.1:8888/RPC2', 'osis_service')
        serializer = ThriftSerializer()
        self.connection = OsisConnection(transport, serializer)

    @q.manage.applicationserver.expose    
    def tags(self, term=None):
        return self.get_items('tag', term)

    @q.manage.applicationserver.expose
    def spaces(self, term=None):
        return self.get_items('space', term)

    @q.manage.applicationserver.expose
    def pages(self, term=None):
        return self.get_items('name', term)

    @q.manage.applicationserver.expose
    def categories(self, term=None):
        return self.get_items('category', term)     
 
    @q.manage.applicationserver.expose 
    def search(self, text=None, space=None, category=None, tags=None):
        # ignore tags for now

        if not any([text, space, category, tags]):
            return []

        sql = ['SELECT view_page_list.category, view_page_list."name", view_page_list.space, view_page_list.guid FROM page.view_page_list WHERE 1=1']
        
        if space:
            sql.append('view_page_list.space = \'%s\'' % space)
  
        if category:
            sql.append('view_page_list.category = \'%s\'', category)

        if text:
            sql.append('view_page_list.content LIKE \'%%%s%%\'' % text)
 
        query = ' AND '.join(sql)

        result = self.connection.page.query(query)

        return result
	
		
    def get_items(self, prop, term=None):

        t = term.split(', ')[-1] if term else ''

        d = {'prop': prop, 'term': t}

        if prop in ('tag',): 
            sql = SQL_PAGE_TAGS_FILTER % d if t else SQL_PAGE_TAGS % d
        else:
            sql = SQL_PAGES_FILTER % d if t else SQL_PAGES % d
   
        q.logger.log('[LFW] sql: %s' % sql, 1)

        qr = self.connection.page.query(sql)

        result = map(lambda _: _[prop], qr)

        return result

    

    


    
