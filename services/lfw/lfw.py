import os.path
from pylabs import q, p
import urllib
import inspect

# @TODO: use sqlalchemy to construct queries - escape values
# @TODO: add space to filter criteria

SQL_PAGES = 'SELECT DISTINCT ui_page.ui_view_page_list.%(prop)s FROM ui_page.ui_view_page_list %(space_criteria)s'
SQL_PAGES_FILTER = 'SELECT DISTINCT ui_page.ui_view_page_list.%(prop)s FROM ui_page.ui_view_page_list WHERE ui_page.ui_view_page_list.%(prop)s LIKE \'%(term)s%%\'  %(space_criteria)s'

SQL_PAGE_TAGS = 'SELECT DISTINCT ui_page.ui_view_page_list.%(prop)s FROM ui_page.ui_view_page_list WHERE ui_page.ui_view_page_list.space=\'%(space)s\''
SQL_PAGE_TAGS_FILTER = 'SELECT DISTINCT ui_page.ui_view_page_list.%(prop)s FROM ui_page.ui_view_page_list WHERE ui_page.ui_view_page_list.space=\'%(space)s\' AND ui_page.ui_view_page_list.%(prop)s LIKE \'%%%(term)s%%\''

class LFWService(object):

    def __init__(self):

        # Initialize API
        self.connection = p.api.model.ui
        self.alkira = q.clients.alkira.getClientByApi(p.api)
        tasklet_path = q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname, 'impl', 'portal')
        self._tasklet_engine = q.taskletengine.get(tasklet_path)
        self._tasklet_engine.addFromPath(os.path.join(q.dirs.baseDir,'lib','python','site-packages','alkira', 'tasklets'))
        self.db_config_path = q.system.fs.joinPaths(q.dirs.cfgDir, 'qconfig', 'dbconnections.cfg')

    @q.manage.applicationserver.expose    
    def tags(self, space=None, term=None):
        results = self.get_items('tags', space=space, term=term)
        final_result = set()
        for item in results:
            tags = item.split(' ')
            for tag in tags:
                if term in tag:
                    final_result.add((tag.strip(',')))
        result = list(final_result)
        return result

    @q.manage.applicationserver.expose
    def spaces(self, term=None, fullInfo=False):
        return self.alkira.listSpaces(fullInfo)

    @q.manage.applicationserver.expose
    def createSpace(self, name, tags=""):
        return self.alkira.createSpace(name, tags.split(' '))
    
    @q.manage.applicationserver.expose
    def deleteSpace(self, name):
        if name == "Admin":
            raise ValueError("Admin space is not deletable")
        
        return self.alkira.deleteSpace(name)
    
    @q.manage.applicationserver.expose
    def updateSpace(self, name, newname=None, tags=""):
        return self.alkira.updateSpace(name, newname, tags.split(' '))
    
    @q.manage.applicationserver.expose
    def pages(self, space=None, term=None):
        return self.alkira.listPages(space)

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
            tags = urllib.unquote_plus(tags)
            tags = tags.strip(', ')
            sql_where.append('ui_view_page_list.tags LIKE \'%%%s%%\'' %  tags)

        if space:
            space = self.alkira.getSpace(space)
            sql_where.append('ui_view_page_list.space = \'%s\'' % space.guid)

        if category:
            sql_where.append('ui_view_page_list.category = \'%s\'' % category)

        if text:
            sql_where.append('ui_view_page_list.content LIKE \'%%%s%%\'' % text)

        query = 'SELECT %s FROM %s WHERE %s' % (sql_select, ' '.join(sql_from), ' AND '.join(sql_where))

        result = self.connection.page.query(query)

        return result

    @q.manage.applicationserver.expose
    def page(self, space, name):
        if not self.alkira.spaceExists(space) or not self.alkira.pageExists(space, name):
            return {}

        page = self.alkira.getPage(space, name)
        props = ['name', 'space', 'category', 'content', 'creationdate', 'title']

        result = dict([(prop, getattr(page, prop)) for prop in props])
        result['tags'] = page.tags.split(' ') if page.tags else []

        return result

    def get_items(self, prop, space=None, term=None):
        if space:
            space = self.alkira.getSpace(space)

        t = term.split(', ')[-1] if term else ''

        d = {'prop': prop, 'space': space, 'term': t}

        if prop in ('tags',):
            sql = SQL_PAGE_TAGS_FILTER % d if t else SQL_PAGE_TAGS % d
        else:
            if t:
                d['space_criteria'] = 'AND ui_view_page_list.space = \'%s\'' % space.guid if space else ''
                sql = SQL_PAGES_FILTER % d
            else:
                d['space_criteria'] = 'WHERE ui_view_page_list.space = \'%s\'' % space.guid if space else ''
                sql = SQL_PAGES % d

        qr = self.connection.page.query(sql)

        result = map(lambda _: _[prop], qr)

        return result

    @q.manage.applicationserver.expose
    def pageTree(self, space, id):
        space = self.alkira.getSpace(space)
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
                """ % {'space': space.guid, 'id': id}

            parent_guid_result = self.connection.page.query(sql1)
            parent_guid = parent_guid_result[0]['guid']
            where = "and pagelist.parent = '%s'" % parent_guid

        sql = """
        SELECT DISTINCT pagelist.guid,
                pagelist.parent,
                pagelist.name,
                pagelist.title,
                pagelist.order,
                (select count(guid) FROM ui_page.ui_view_page_list WHERE ui_page.ui_view_page_list.parent = pagelist.guid) as nrofkids
                FROM ONLY ui_page.ui_view_page_list as pagelist
                WHERE pagelist.space = '%(space)s' %(where)s ORDER BY pagelist.order, pagelist.title;
        """ % {'space': space.guid, 'where': where}

        result = self.connection.page.query(sql)
        data = list()
        for node in result :
            if node['name'] == 'pagetree':
                continue
            nodedata = dict()
            children = list()
            state = 'closed' if node['nrofkids'] > 0 else 'leaf'
            nodedata = {'data': {'title': node['title'],
                                 'type': 'link',
                                 'attr': {'href': '#/%s/%s' % (space.name, node['name'])},
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
    def generic(self, tagstring=None, macroname=None, params=None):
        q.logger.log('[GENERIC] Request tagstring: %s' % tagstring, 5)
        params = params or dict()
        tags = q.base.tags.getObject(tagstring)

        params['tags'] = tags

        self._tasklet_engine.execute(params=params, tags=('pylabsmacro', macroname, ))

        result = params.get('result', '')
        q.logger.log('[GENERIC] Result: %s' % result, 5)

        return result

    @q.manage.applicationserver.expose
    def importSpace(self, space, filename):
        import tarfile
        def filterFiler(filename):
            return (filename.startswith("/") or filename.startswith(".."))
        q.logger.log('importing file %s for space %s' % (filename,space), 5)
        appname = p.api.appname
        tarFile = tarfile.open(filename)
        invalidlinks = filter(filterFiler, tarFile.getnames())
        if invalidlinks:
            #Prepare error message
            if len(invalidlinks) > 15:
                invalidlinks = invalidlinks[:14]
                invalidlinks.append("...")
            raise ValueError("File names must be relative, please remove the following files\n"%"\n".join(invalidlinks))
        dest = q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, "portal", "spaces")
        q.system.fs.removeDirTree(q.system.fs.joinPaths(dest, space))
        tarFile.extractall(dest)
        p.application.syncPortal(appname, space)
        tarFile.close()

    @q.manage.applicationserver.expose
    def exportSpace(self, space, filename):
        if q.system.fs.exists(filename):
            q.system.fs.removeFile(filename)
        import tarfile
        q.logger.log('exporting space %s to file %s' % (space, filename), 5)
        appname = p.api.appname
        tarFile = tarfile.open(filename, mode="w|gz")
        dest = q.system.fs.joinPaths(q.dirs.pyAppsDir, appname,"portal", "spaces", space)
        tarFile.add(dest, space)
        tarFile.close()

    @q.manage.applicationserver.expose
    def hgPush(self, spaceGuid, repository, username=None):
        if not repository:
            return "Please give a repository to push to."

        spaceInfo = self.alkira.getSpace(spaceGuid)

        #check if we need to update the repo in osis
        if repository != spaceInfo.repository:
            self.alkira.updateSpace(spaceGuid, repository=repository)

        hg = q.clients.mercurial.getclient(q.dirs.pyAppsDir + "/" + p.api.appname + "/portal/spaces/" + spaceInfo.name,
            repository.encode("utf-8"))

        #check if we already have the latest version
        retval, msg = hg._hgCmdExecutor("incoming", source=hg.getUrl(), die=False, autoCheckFix=False)
        if retval == 1 and "no changes found" in msg: #no changes we can push
            if username:
                #set the username for the commit
                hg._ui.environ["HGUSER"] = username
            hg.pushcommit("automated commit by Alkira", addRemoveUntrackedFiles=True)
            return True
        else:
            return False

    @q.manage.applicationserver.expose
    def hgPull(self, spaceGuid, repository, dontSync=False):
        if not repository:
            return "Please give a repository to pull from."

        spaceInfo = self.alkira.getSpace(spaceGuid)

        #check if we need to update the repo in osis
        if repository != spaceInfo.repository:
            self.alkira.updateSpace(spaceGuid, repository=repository)

        #pull everything
        hg = q.clients.mercurial.getclient(q.dirs.pyAppsDir + "/" + p.api.appname + "/portal/spaces/" + spaceInfo.name,
            repository.encode("utf-8"))
        hg.pullupdate()

        #resync pages
        if not dontSync:
            p.application.syncPortal(p.api.appname)

        return True
