from pymonkey import q
import osis
from osis.client import OsisConnection
from osis.client.xmlrpc import XMLRPCTransport
from osis.model.serializers import ThriftSerializer

import time


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

        sql_select = 'view_page_list.category, view_page_list."name", view_page_list.space'
        sql_from = ['page.view_page_list']
        sql_where = ['1=1']

        if tags:
            taglist = tags.split(', ') or []
            
            for x, tag in enumerate(taglist):
               sql_from.append('INNER JOIN page.view_page_tag_list tl%(x)s ON tl%(x)s.guid = view_page_list.guid AND tl%(x)s.tag = \'%(tag)s\'' % {'tag': tag, 'x': x})

        if space:
            sql_where.append('view_page_list.space = \'%s\'' % space)
  
        if category:
            sql_where.append('view_page_list.category = \'%s\'' % category)

        if text:
            sql_where.append('view_page_list.content LIKE \'%%%s%%\'' % text)
 
        query = 'SELECT %s FROM %s WHERE %s' % (sql_select, ' '.join(sql_from), ' AND '.join(sql_where))

        result = self.connection.page.query(query)

        return result

    @q.manage.applicationserver.expose
    def page(self, space, name):
        sql = """
              SELECT 
                  view_page_list.guid 
              FROM 
                  page.view_page_list 
              WHERE 
                  page.view_page_list.space = \'%(space)s\' 
                  AND 
                  page.view_page_list."name" = \'%(name)s\'""" % {'space': space, 'name': name}


        qr = self.connection.page.query(sql)
  
        if not qr:
            return {}

        page = self.connection.page.get(qr[0]['guid'])
        props = ['name', 'space', 'category', 'content', 'creationdate']

        result = dict([(prop, getattr(page, prop)) for prop in props]) 
        result['tags'] = page.tags.split(' ') 

        return result

    def get_items(self, prop, term=None):

        t = term.split(', ')[-1] if term else ''

        d = {'prop': prop, 'term': t}

        if prop in ('tag',): 
            sql = SQL_PAGE_TAGS_FILTER % d if t else SQL_PAGE_TAGS % d
        else:
            sql = SQL_PAGES_FILTER % d if t else SQL_PAGES % d

        qr = self.connection.page.query(sql)

        result = map(lambda _: _[prop], qr)

        return result

    @q.manage.applicationserver.expose
    def pageTree(self, space):
        sql = """
        SELECT DISTINCT pagelist.guid,
                pagelist.name,
                pagelist.content,
                pagelist.parent,
                pagelist.category
                FROM ONLY page.view_page_list pagelist
                WHERE pagelist.space = '%(space)s'
                    AND pagelist.guid in (
                                            WITH RECURSIVE childpages AS
                                            (
                                                    -- non-recursive term
                                                    SELECT page.view_page_list.guid
                                                    FROM page.view_page_list

                                                    UNION ALL

                                                -- recursive term
                                                SELECT pl.guid
                                                FROM page.view_page_list AS pl
                                                JOIN
                                                    childpages AS cp
                                                    ON (pl.parent = cp.guid)
                                            )
                                            SELECT guid FROM childpages
                                         );
        """ % {'space': space}

        return self.connection.page.query(sql)

    @q.manage.applicationserver.expose
    def query(self, sql, rows, dbname='', link='', _search='', nd='', page=1, sidx='', sord='', applicationserver_request='', *args, **kwargs):
        cfgfilepath = q.system.fs.joinPaths(q.dirs.cfgDir, 'qconfig', 'dbconnections.cfg')
        if q.system.fs.exists(cfgfilepath):
            inifile = q.tools.inifile.open(cfgfilepath)
            section = 'db_%s' % dbname
            if inifile.checkSection(section):
                dbserver = inifile.getValue(section, 'dbserver')
                dblogin = inifile.getValue(section, 'dblogin')
                dbpassword = inifile.getValue(section, 'dbpassword')
                dbname = inifile.getValue(section, 'dbname')
                if dbname not in q.manage.postgresql8.cmdb.databases:
                    q.manage.postgresql8.startChanges()
                    q.manage.postgresql8.cmdb.addDatabase(dbname, 'qbase')
                    if dblogin not in q.manage.postgresql8.cmdb.databases:
                        q.manage.postgresql8.cmdb.addLogin(dblogin, cidr_address=dbserver)
                    q.manage.postgresql8.applyConfig()
                    sqldata = q.cmdtools.postgresql8.query._executeSQL(dblogin, sql, database=dbname)
        else:
            connection = self.connection
        sqldata = connection.page.query(sql)
        data = dict()
        
        data['columns'] = sqldata[0].keys()
        data['page'] = page
        data['total'] = len(sqldata) / rows
        data['records'] = rows
        data['rows'] = list()
        start = (int(page) - 1) * int(rows)
        end = (int(page) - 1) * (rows) + (rows)
        for index, pageobj in enumerate(sqldata[start:end]):
            data['rows'].append({'id': index + 1, 'cell': pageobj.values()})
        return data


    @q.manage.applicationserver.expose
    def graphviz(self, graphDot_str, applicationserver_request=''):
        import pygraphviz as pgv

        graphDot_str = graphDot_str.replace("&gt;", ">")
        G = pgv.AGraph(graphDot_str)
        G.layout(prog='dot')
        filename = "%s.gif" % (int(time.time()))
        path = q.system.fs.joinPaths(q.dirs.baseDir, "www", "img", filename)
        G.draw(path)
        q.system.unix.chmod(q.system.fs.getDirName(path), 0755, filePattern="*.gif")
        path_uri = path.replace("/opt/qbase3/www/", "")
        return path_uri


