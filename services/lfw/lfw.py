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
    def pageTree(self, space):
        sql = """
        SELECT DISTINCT pagelist.guid,
                pagelist.name,
                pagelist.content,
                pagelist.parent,
                pagelist.category
                FROM ONLY ui_page.ui_view_page_list pagelist
                WHERE pagelist.space = '%(space)s'
                    AND pagelist.guid in (
                                            WITH RECURSIVE childpages AS
                                            (
                                                    -- non-recursive term
                                                    SELECT ui_page.ui_view_page_list.guid
                                                    FROM ui_page.ui_view_page_list

                                                    UNION ALL

                                                -- recursive term
                                                SELECT pl.guid
                                                FROM ui_page.ui_view_page_list AS pl
                                                JOIN
                                                    childpages AS cp
                                                    ON (pl.parent = cp.guid)
                                            )
                                            SELECT guid FROM childpages
                                         );
        """ % {'space': space}

        return self.connection.page.query(sql)
    
    @q.manage.applicationserver.expose
    def query(self, sql, rows, dbname, applicationserver_request='', *args, **kwargs):
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
        data['page'] = 1
        data['total'] = len(sqldata) / rows
        data['records'] = rows
        data['rows'] = list()
        for index, page in enumerate(sqldata):
            data['rows'].append({'id': index + 1, 'cell': page.values()})
        return data


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