import os.path
from pylabs import q, p
import urllib

# @TODO: use sqlalchemy to construct queries - escape values 
# @TODO: add space to filter criteria

SQL_PAGES = 'SELECT DISTINCT ui_page.ui_view_page_list.%(prop)s FROM ui_page.ui_view_page_list %(space_criteria)s'
SQL_PAGES_FILTER = 'SELECT DISTINCT ui_page.ui_view_page_list.%(prop)s FROM ui_page.ui_view_page_list WHERE ui_page.ui_view_page_list.%(prop)s LIKE \'%(term)s%%\'  %(space_criteria)s'

SQL_PAGE_TAGS = 'SELECT DISTINCT ui_page.ui_view_page_tag_list.%(prop)s FROM ui_page.ui_view_page_tag_list'
SQL_PAGE_TAGS_FILTER = 'SELECT DISTINCT ui_page.ui_view_page_tag_list.%(prop)s FROM ui_page.ui_view_page_tag_list WHERE ui_page.ui_view_page_tag_list.%(prop)s LIKE \'%(term)s%%\''

class LFWService(object):

    def __init__(self, tasklet_path=None):
        
        # Initialize API
        self.connection = p.api.model.core
        self.db_config_path = q.system.fs.joinPaths(q.dirs.cfgDir, 'qconfig', 'dbconnections.cfg')
        module = os.path.abspath(os.path.dirname(__file__))
        tasklet_path = os.path.abspath(os.path.join(module, 'tasklets'))
        self._tasklet_engine = q.taskletengine.get(tasklet_path)
        self._tasklet_engine.addFromPath(os.path.join(q.dirs.baseDir,'lib','python','site-packages','alkira', 'tasklets'))

    @q.manage.applicationserver.expose    
    def tags(self, term=None):
        return self.get_items('tag', term)

    @q.manage.applicationserver.expose
    def spaces(self, term=None):
        return self.get_items('space', term)

    @q.manage.applicationserver.expose
    def pages(self, space=None, term=None):
        return self.get_items('name', space, term)

    @q.manage.applicationserver.expose
    def categories(self, space=None, term=None):
        return self.get_items('category', space, term)
 
    @q.manage.applicationserver.expose 
    def search(self, text=None, space=None, category=None, tags=None):
        # ignore tags for now

        if not any([text, space, category, tags]):
            return []

        sql_select = 'ui_view_page_list.category, ui_view_page_list."name", ui_view_page_list.space'
        sql_from = ['ui_page.ui_view_page_list']
        sql_where = ['1=1']

        if tags:
            # MNour - A hackish solution for tags/labels search. @see PYLABS-14.
            # MNOUR - IMO this should be solved in the REST layer.
            taglist = [tag for tag in urllib.unquote_plus(tags).split(', ') if tag] or []

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
                  ui_page.ui_view_page_list.guid 
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
        result['tags'] = page.tags.split(' ') if page.tags else []

        return result

    def get_items(self, prop, space=None, term=None):

        t = term.split(', ')[-1] if term else ''

        d = {'prop': prop, 'term': t}

        if prop in ('tag',):
            sql = SQL_PAGE_TAGS_FILTER % d if t else SQL_PAGE_TAGS % d
        else:
            if t:
                d['space_criteria'] = 'AND ui_view_page_list.space = \'%s\'' % space if space else ''
                sql = SQL_PAGES_FILTER % d
            else:
                d['space_criteria'] = 'WHERE ui_view_page_list.space = \'%s\'' % space if space else ''
                sql = SQL_PAGES % d

        qr = self.connection.page.query(sql)

        result = map(lambda _: _[prop], qr)

        return result

    @q.manage.applicationserver.expose
    def pageTree(self, space, id):
        where = ""
        if id == 0:
            where = "and pagelist.parent is null"  
        elif q.basetype.guid.check(id):
            where = "and pagelist.parent = '%s'" % id 
        else:
            sql1 = """
                SELECT DISTINCT pagelist.guid 
                FROM ONLY ui_page.ui_view_page_list as pagelist
                WHERE pagelist.space ='%(space)s' and pagelist.name = '%(id)s';
                """ % {'space': space, 'id': id}
            
            parent_guid_result = self.connection.page.query(sql1)
            parent_guid = parent_guid_result[0]['guid']
            where = "and pagelist.parent = '%s'" % parent_guid

        sql = """
        SELECT DISTINCT pagelist.guid,
                pagelist.parent,
                pagelist.name,
                (select count(guid) FROM ui_page.ui_view_page_list WHERE ui_page.ui_view_page_list.parent = pagelist.guid) as nrofkids
                FROM ONLY ui_page.ui_view_page_list as pagelist
                WHERE pagelist.space = '%(space)s' %(where)s ORDER BY pagelist.name;
        """ % {'space': space, 'where': where}

        result = self.connection.page.query(sql)
        data = list()
        for node in result :
            if node['name'] == 'pagetree':
                continue
            nodedata = dict()
            children = list()
            state = 'closed' if node['nrofkids'] > 0 else 'leaf'
            nodedata = {'data': {'title': node['name'],
                                 'type': 'link',
                                 'attr': {'href': '#/%s/%s' % (space, node['name'])},
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
    def query(self, sqlselect, rows, table, schema, dbconnection='', link='', _search='', nd='', page=1, sidx='', sord='', applicationserver_request='', *args, **kwargs):
        import sqlalchemy
        from sqlalchemy import MetaData, Table, create_engine
        from sqlalchemy.orm import sessionmaker
        import math
        import re

        localdb = False
        cfgfilepath = self.db_config_path
        q.logger.log('FILE IS %s' % cfgfilepath, 1)
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
            dbname = 'sampleapp'
            dbserver = '127.0.0.1'
            dblogin = q.manage.postgresql8.cmdb.rootLogin
            dbpassword = q.manage.postgresql8.cmdb.rootPasswd

        start = (int(page) - 1) * int(rows)
        pagefields = list()

        #sqlalchemy stuff
        engine = create_engine('postgresql://%s:%s@%s/%s' % (dblogin, dbpassword, dbserver, dbname))
        connection = engine.connect()

        comp = re.compile(".*from(?P<end>.*)", re.I)
        countquery = comp.sub("select count(*) as count from \g<end>", sqlselect)
        if sidx:
            sqlselect += " ORDER BY %s %s" % (sidx, sord)
        sqlselect += ' LIMIT %s OFFSET %s' % (rows, start)
        
        t = engine.text(countquery)
        totalrowcount = t.execute().fetchone()[0]
        t = engine.text(sqlselect)
        output = t.execute()
        result = output.fetchall()

        data = dict()
        data['columns'] = output.keys()
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
        G = pgv.AGraph(string=graphDot_str)
        G.layout(prog='dot')
        rawimage = StringIO.StringIO()
        G.draw(rawimage, 'gif')
        rawimage.buf = ''
        img_b64 = base64.b64encode(rawimage.getvalue())
        return img_b64

    @q.manage.applicationserver.expose
    def generic(self, tagstring=None, macroname=None):
        q.logger.log('[GENERIC] Request tagstring: %s' % tagstring, 5)

        tags = q.base.tags.getObject(tagstring)

        params = {
        'tags': tags,
        }

        self._tasklet_engine.execute(params=params, tags=('pylabsmacro', macroname, ))

        result = params.get('result', '')
        q.logger.log('[GENERIC] Result: %s' % result, 5)

        return result
