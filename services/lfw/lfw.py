import os.path

from pylabs import q, p

# @TODO: use sqlalchemy to construct queries - escape values 
# @TODO: add space to filter criteria

SQL_PAGES = 'SELECT DISTINCT ui_page.ui_view_page_list.%(prop)s FROM ui_page.ui_view_page_list'
SQL_PAGES_FILTER = 'SELECT DISTINCT ui_page.ui_view_page_list.%(prop)s FROM ui_page.ui_view_page_list WHERE ui_page.ui_view_page_list.%(prop)s LIKE \'%(term)s%%\''

SQL_PAGE_TAGS = 'SELECT DISTINCT ui_page.ui_view_page_tag_list.%(prop)s FROM ui_page.ui_view_page_tag_list'
SQL_PAGE_TAGS_FILTER = 'SELECT DISTINCT ui_page.ui_view_page_tag_list.%(prop)s FROM ui_page.ui_view_page_tag_list WHERE ui_page.ui_view_page_tag_list.%(prop)s LIKE \'%(term)s%%\''


class LFWService(object):

    def __init__(self, tasklet_path=None):
        
        # Initialize API
        self.connection = p.api.model.core

        module = os.path.abspath(os.path.dirname(__file__))
        tasklet_path = os.path.abspath(os.path.join(module, 'tasklets'))
        self._tasklet_engine = q.taskletengine.get(tasklet_path)

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

        sql_select = 'ui_view_page_list.category, ui_view_page_list."name", ui_view_page_list.space'
        sql_from = ['ui_page.ui_view_page_list']
        sql_where = ['1=1']

        if tags:
            taglist = tags.split(', ') or []
            
            for x, tag in enumerate(taglist):
               sql_from.append('INNER JOIN ui_page.ui_view_page_tag_list tl%(x)s ON tl%(x)s.guid = ui_view_page_list.guid AND tl%(x)s.tag = \'%(tag)s\'' % {'tag': tag, 'x': x})

        if space:
            sql_where.append('ui_view_page_list.space = \'%s\'' % space)
  
        if category:
            sql_where.append('ui_view_page_list.category = \'%s\'' % category)

        if text:
            sql_where.append('ui_view_page_list.content LIKE \'%%%s%%\'' % text)
 
        query = 'SELECT %s FROM %s WHERE %s' % (sql_select, ' '.join(sql_from), ' AND '.join(sql_where))

        result = self.connection.page.query(query)

        return result

    @q.manage.applicationserver.expose
    def page(self, space, name):
        sql = """
              SELECT 
                  ui_view_page_list.guid 
              FROM 
                  ui_page.ui_view_page_list 
              WHERE 
                  ui_page.ui_view_page_list.space = \'%(space)s\' 
                  AND 
                  ui_page.ui_view_page_list."name" = \'%(name)s\'""" % {'space': space, 'name': name}


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
    def pageTree(self, space, id):
        where = ""
        if id == 0:
            where = "and pagelist.parent is null"  
        else:
            where = "and pagelist.parent = '%s'" % id 
            
        sql = """
        SELECT DISTINCT pagelist.guid,
                pagelist.parent,
                pagelist.name,
                (select count(guid) FROM page.view_page_list WHERE page.ui_view_page_list.parent = pagelist.guid) as nrofkids
                FROM ONLY page.ui_view_page_list as pagelist
                WHERE pagelist.space = '%(space)s' %(where)s;
        """ % {'space': space, 'where': where}

        result = self.connection.page.query(sql)
        data = list()
        for node in result:
            
            nodedata = dict()
            children = list()
            state = 'closed' if node['nrofkids'] > 0 else 'leaf'
            nodedata = {'data': {'title': node['name'],
                                 'type': 'link',
                                 'attr': {'href': '/#/%s/%s' % (space, node['name'])},
                                 'children':[]
                                 },
                        'attr': {
                                 'class': 'TreeTitle',
                                 'id': node['guid']
                                },
                        'state' : state
                        }
            data.append(nodedata)
        q.logger.log(data, 1)
        return data

    
    @q.manage.applicationserver.expose
    def query(self, fields, rows, table, schema, dbconnection='', link='', _search='', nd='', page=1, sidx='', sord='', applicationserver_request='', *args, **kwargs):
        import sqlalchemy
        from sqlalchemy import MetaData, Table, create_engine
        from sqlalchemy.orm import sessionmaker
        import math

        localdb = False
        cfgfilepath = q.system.fs.joinPaths(q.dirs.cfgDir, 'qconfig', 'dbconnections.cfg')
        if q.system.fs.exists(cfgfilepath):
            inifile = q.tools.inifile.open(cfgfilepath)
            section = 'db_%s' % dbconnection
            if inifile.checkSection(section):
                dbserver = inifile.getValue(section, 'dbserver')
                dblogin = inifile.getValue(section, 'dblogin')
                dbpassword = inifile.getValue(section, 'dbpasswd')
                dbname = inifile.getValue(section, 'dbname')
            else:
                localdb = True
        else:
            localdb = True
        if localdb:
            dbname = 'portal'
            dbserver = '127.0.0.1'
            dblogin = q.manage.postgresql8.cmdb.rootLogin
            dbpassword = q.manage.postgresql8.cmdb.rootPasswd

        start = (int(page) - 1) * int(rows)
        fields = fields.split(',')
        pagefields = list()

        #sqlalchemy stuff
        engine = create_engine('postgresql://%s:%s@%s/%s' % (dblogin, dbpassword, dbserver, dbname))
        Session = sessionmaker()
        Session.configure(bind=engine)
        session = Session(bind=engine)
        metadata = MetaData(engine)
        tableobj = Table(table, metadata, autoload=True, schema=schema)
        totalrowcount = session.query(tableobj, getattr(tableobj.c, fields[0])).count()

        for field in fields:
            pagefields.append(getattr(tableobj.c, field))
        if sidx:
            selection = sqlalchemy.select(pagefields, limit=rows, offset=start, order_by=[getattr(tableobj.c.name, sord)()])
        else:
            selection = sqlalchemy.select(pagefields, limit=rows, offset=start)
        output = selection.execute()
        result = output.fetchall()

        data = dict()
        data['columns'] = fields
        data['page'] = page
        data['total'] = int(math.ceil(totalrowcount/float(rows)))
        data['records'] = rows
        data['rows'] = list()

        for index, pageobj in enumerate(result):
            data['rows'].append({'id': index + 1, 'cell': list(pageobj)})
        return data

    @q.manage.applicationserver.expose
    def graphviz(self, graphDot_str, applicationserver_request=''):
        import pygraphviz as pgv
        import base64
        import StringIO

        graphDot_str = graphDot_str.replace("&gt;", ">")
        G = pgv.AGraph(graphDot_str)
        G.layout(prog='dot')
        rawimage = StringIO.StringIO()
        G.draw(rawimage, 'gif')
        img_b64 = base64.b64encode(rawimage.getvalue())
        return img_b64

    @q.manage.applicationserver.expose
    def generic(self, tagstring=None):
        q.logger.log('[GENERIC] Request tagstring: %s' % tagstring, 5)

        tags = q.base.tags.getObject(tagstring)

        params = {
            'tags': tags,
        }

        self._tasklet_engine.execute(params=params, tags=('macro', 'generic', ))

        result = params.get('result', '')
        q.logger.log('[GENERIC] Result: %s' % result, 5)

        return result