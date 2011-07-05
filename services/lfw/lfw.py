import os
import os.path
from pylabs import q, p
import urllib
import inspect
import functools
import json

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

    @q.manage.applicationserver.expose_authenticated
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

    @q.manage.applicationserver.expose_authenticated
    def spaces(self, term=None):
        return self.alkira.listSpaces()

    @q.manage.applicationserver.expose_authenticated
    def createSpace(self, name, tags=""):
        self.alkira.createSpace(name, tags.split(' '))

    @q.manage.applicationserver.expose_authenticated
    def deleteSpace(self, name):
        if name == "Admin":
            raise ValueError("Admin space is not deletable")

        self.alkira.deleteSpace(name)

    @q.manage.applicationserver.expose_authenticated
    def users(self, username=None):
        return self.alkira.listUsers(username)

    @q.manage.applicationserver.expose_authenticated
    def createUser(self, name, password, tags=""):
        self.alkira.createUser(name, password, tags.split(' '))

    @q.manage.applicationserver.expose_authenticated
    def deleteUser(self, name):
        self.alkira.deleteUser(name)

    @q.manage.applicationserver.expose_authenticated
    def updateUser(self, name, newname=None, tags=""):
        self.alkira.updateUser(name, newname, tags.split(' '))

    @q.manage.applicationserver.expose_authenticated
    def pages(self, space=None, term=None):
        return self.alkira.listPages(space)

    @q.manage.applicationserver.expose_authenticated
    def categories(self, space=None, term=None):
        return self.get_items('category', space, term)

    @q.manage.applicationserver.expose_authenticated
    def search(self, text=None, space=None, category=None, tags=None):
        # ignore tags for now

        if not any([text, space, category, tags]):
            return []

        sql_select = 'page.category, page."name", space.name as space'
        sql_from = 'ui_page.ui_view_page_list as page join ui_space.ui_view_space_list as space on page.space = space.guid'
        sql_where = ['1=1']

        if tags:
            # MNour - A hackish solution for tags/labels search. @see PYLABS-14.
            # MNOUR - IMO this should be solved in the REST layer.
            tags = urllib.unquote_plus(tags)
            tags = tags.strip(', ')
            sql_where.append('page.tags LIKE \'%%%s%%\'' %  tags)

        if space:
            space = self.alkira.getSpace(space)
            sql_where.append('page.space = \'%s\'' % space.guid)

        if category:
            sql_where.append('page.category = \'%s\'' % category)

        if text:
            sql_where.append('page.content LIKE \'%%%s%%\'' % text)

        query = 'SELECT %s FROM %s WHERE %s' % (sql_select, sql_from, ' AND '.join(sql_where))

        result = self.connection.page.query(query)

        return result

    def _breadcrumbs(self, page):
        breadcrumbs = []
        parent = page
        while parent:
            breadcrumbs.append({'guid': parent.guid,
                                'name': parent.name,
                                'title': parent.title})
            parent = self.alkira.getPageByGUID(parent.parent) if parent.parent else None

        breadcrumbs.reverse()
        return breadcrumbs

    @q.manage.applicationserver.expose_authenticated
    def breadcrumbs(self, space, name):
        return self._breadcrumbs(self.alkira.getPage(space, name))

    @q.manage.applicationserver.expose_authenticated
    def page(self, space, name):
        if not self.alkira.spaceExists(space) or not self.alkira.pageExists(space, name):
            return {"code": 404,
                    "error": "Page Not Found"}

        page = self.alkira.getPage(space, name)
        props = ['name', 'space', 'category', 'content', 'creationdate', 'title', 'pagetype']

        result = dict([(prop, getattr(page, prop)) for prop in props])
        result['tags'] = page.tags.split(' ') if page.tags else []

        return result

    def _syncPageToDisk(self, space, page, oldpagename=None):
        crumbs = self._breadcrumbs(page)
        _join = q.system.fs.joinPaths
        _isfile = q.system.fs.isFile
        _isdir = q.system.fs.isDir
        _write = q.system.fs.writeFile

        dir = _join(q.dirs.baseDir, "pyapps", p.api.appname, "portal", "spaces", space)
        upper = dir
        for i, level in enumerate(crumbs):
            name, _, ext = level['name'].rpartition('.')
            file = _join(dir, level['name'])
            dir = _join(dir, name)

            if i == len(crumbs) - 1:
                if oldpagename:
                    oldname, _, ext = oldpagename.rpartition('.')
                    oldfile = _join(upper, oldpagename)
                    olddir = _join(upper, oldname)
                    tofile = file
                    if _isdir(olddir):
                        oldfile = _join(olddir, oldpagename)
                        tofile = _join(olddir, level['name'])

                    if _isfile(oldfile):
                        q.system.fs.renameFile(oldfile, tofile)
                    if _isdir(olddir):
                        q.system.fs.renameDir(olddir, dir)

                if _isdir(dir):
                    file = _join(dir, level['name'])
                _write(file, page.content)
            else:
                #in the chain
                if _isfile(file):
                    tmp = os.tmpnam()
                    q.system.fs.renameFile(file, tmp)
                    q.system.fs.createDir(dir)
                    q.system.fs.renameFile(tmp, _join(dir, level['name']))

            upper = dir

    def _syncPageDelete(self, space, crumbs):
        _join = q.system.fs.joinPaths
        _isfile = q.system.fs.isFile
        _isdir = q.system.fs.isDir

        dir = _join(q.dirs.baseDir, "pyapps", p.api.appname, "portal", "spaces", space)
        for i, level in enumerate(crumbs):
            name, _, ext = level['name'].rpartition('.')
            file = _join(dir, level['name'])
            dir = _join(dir, name)
            if i == len(crumbs) - 1:
                if _isdir(dir):
                    q.system.fs.removeDirTree(dir)
                elif _isfile(file):
                    q.system.fs.removeFile(file)


    @q.manage.applicationserver.expose_authenticated
    def createPage(self, space, name, content, parent=None, order=None, title=None, tags="", category='portal', pagetype="md"):
        if self.alkira.pageExists(space, name):
            raise ValueError("A page with the same name already exists")

        page = self.alkira.createPage(space=space, name=name, content=content, parent=parent, order=order, title=title, tagsList=tags.split(" "), category=category, pagetype=pagetype)
        #self._syncPageToDisk(space, page)

    @q.manage.applicationserver.expose_authenticated
    def updatePage(self, space, name, content, newname=None, parent=None, order=None, title=None, tags="", category=None, pagetype=None):
        if not self.alkira.pageExists(space, name):
            raise ValueError("Page '%s' doesn't exists" % name)

        if newname and newname != name:
            if self.alkira.pageExists(space, newname):
                raise ValueError("Page '%s' already exists" % newname)

        page = self.alkira.updatePage(old_space=space, old_name=name, name=newname,
                               content=content, parent=parent, order=order, title=title, tagsList=tags.split(" "), category=category, pagetype=pagetype)

        #self._syncPageToDisk(space, page, name)

    @q.manage.applicationserver.expose_authenticated
    def deletePage(self, space, name):
        crumbs = self.breadcrumbs(space, name)
        self.alkira.deletePageAndChildren(space, name)
        self._syncPageDelete(space, crumbs)

    def get_items(self, prop, space=None, term=None):
        if space:
            space = self.alkira.getSpace(space)

        t = term.split(', ')[-1] if term else ''

        d = {'prop': prop, 'space': space.guid, 'term': t}

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

    @q.manage.applicationserver.expose_authenticated
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


    @q.manage.applicationserver.expose_authenticated
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

    @q.manage.applicationserver.expose_authenticated
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

    @q.manage.applicationserver.expose_authenticated
    def generic(self, tagstring=None, macroname=None, params=None):
        q.logger.log('[GENERIC] Request tagstring: %s' % tagstring, 5)
        params = params or dict()
        tags = q.base.tags.getObject(tagstring)

        params['tags'] = tags

        self._tasklet_engine.execute(params=params, tags=('pylabsmacro', macroname, ))

        result = params.get('result', '')
        q.logger.log('[GENERIC] Result: %s' % result, 5)

        return result

    @q.manage.applicationserver.expose_authenticated
    def importSpace(self, space, filename, cleanImport = False):
        join = q.system.fs.joinPaths
        import tarfile
        def filterFiler(filename):
            return (filename.startswith("/") or filename.startswith(".."))
        q.logger.log('importing file %s for space %s' % (filename,space), 5)
        appname = p.api.appname
        client = q.clients.alkira.getClient("localhost", appname)
        tarFile = tarfile.open(filename)
        invalidlinks = filter(filterFiler, tarFile.getnames())
        if invalidlinks:
            #Prepare error message
            if len(invalidlinks) > 15:
                invalidlinks = invalidlinks[:14]
                invalidlinks.append("...")
            raise ValueError("File names must be relative, please remove the following files\n"%"\n".join(invalidlinks))
        dest = join(q.dirs.pyAppsDir, appname, "portal", "spaces", space)
        #if the space already exists, I should remove it first
        if client.spaceExists(space) and cleanImport:
            q.system.fs.removeDirTree(dest)
            q.system.fs.createDir(dest)
        tarFile.extractall(join(dest, ""))
        tarFile.close()
        p.application.syncPortal(appname, space)

    @q.manage.applicationserver.expose_authenticated
    def exportSpace(self, space, filename):
        join = q.system.fs.joinPaths
        def buildTree(client, path, space, pagenams = None):
            if not pagenams:
                pagenams = client.listChildPages(space)

            for pagename in pagenams:
                chidpages = client.listChildPages(space, pagename)
                pagepath = join(path, pagename)
                q.system.fs.createDir(pagepath)
                if chidpages:
                    buildTree(client, pagepath, space, chidpages)
                page = client.getPage(space, pagename)
                filename = join(pagepath, pagename + ".md")
                fpage = open(filename, "w")
                fpage.write("@metadata title = %s\n"%page.title)
                fpage.write("@metadata order = %s\n"%page.order)
                fpage.write("@metadata tagstring = %s\n"%str(page.tags))
                fpage.write(page.content)
                fpage.close()

        q.logger.log('exporting space %s to file %s' % (space, filename), 5)
        appname = p.api.appname
        client = q.clients.alkira.getClient("localhost", appname)
        tempdir = join(q.dirs.tmpDir, space)
        buildTree(client, tempdir, space)
        import tarfile
        tarFile = tarfile.open(filename, mode="w|gz")
        tarFile.add(tempdir, "")
        tarFile.close()
        q.system.fs.removeDirTree(tempdir)

    def hgCheckInfo(self, space, repository, repo_username, repo_password):
        if space.repository.url != repository or space.repository.username != repo_username or \
            (repo_password and space.repository.password != repo_password):

            self.alkira.updateSpace(space.guid, repository=repository, repo_username=repo_username,
                repo_password=repo_password)
            return True
        return False

    def createRepoUrl(self, repo):
        from urlparse import urlsplit, urlunsplit
        url = urlsplit(repo.url)
        return urlunsplit((url.scheme, "%s:%s@%s" % (repo.username, repo.password, url.netloc), url.path, url.query,
            url.fragment))

    @q.manage.applicationserver.expose_authenticated
    def hgPushSpace(self, space, repository, repo_username, repo_password=None):
        if not repository:
            return "Please give a repository to push to."

        spaceInfo = self.alkira.getSpace(space)

        #check if we need to update the repo in osis
        if self.hgCheckInfo(spaceInfo, repository, repo_username, repo_password):
            #update to reflect changes
            spaceInfo = self.alkira.getSpace(space)

        repoUrl = self.createRepoUrl(spaceInfo.repository)

        q.logger.log('pushing space %s to %s' % (spaceInfo.name, spaceInfo.repository.url), 5)

        hg = q.clients.mercurial.getclient(q.dirs.pyAppsDir + "/" + p.api.appname + "/portal/spaces/" + spaceInfo.name,
            repoUrl)

        #check if we already have the latest version
        retval, msg = hg._hgCmdExecutor("incoming", source=hg.getUrl(), die=False, autoCheckFix=False)
        if retval == 1 and "no changes found" in msg: #no changes we can push
            #set the username for the commit
            hg._ui.environ["HGUSER"] = spaceInfo.repository.username
            hg.pushcommit("automated commit by Alkira", addRemoveUntrackedFiles=True)
            return True
        else:
            return False

    @q.manage.applicationserver.expose_authenticated
    def hgPullSpace(self, space, repository, repo_username, repo_password=None, dontSync=False):
        if not repository:
            return "Please give a repository to pull from."

        spaceInfo = self.alkira.getSpace(space)

        #check if we need to update the repo in osis
        if self.hgCheckInfo(spaceInfo, repository, repo_username, repo_password):
            #update to reflect changes
            spaceInfo = self.alkira.getSpace(space)

        repoUrl = self.createRepoUrl(spaceInfo.repository)

        #pull everything
        q.logger.log('pulling space %s from %s' % (spaceInfo.name, spaceInfo.repository.url), 5)
        hg = q.clients.mercurial.getclient(q.dirs.pyAppsDir + "/" + p.api.appname + "/portal/spaces/" + spaceInfo.name,
            repoUrl)
        hg.pullupdate()

        #resync pages for space
        if not dontSync:
            p.application.syncPortal(p.api.appname, space=spaceInfo.name)

        return True

    @q.manage.applicationserver.expose_authenticated
    def space(self, space):
        if not self.alkira.spaceExists(space):
            return {}

        space = self.alkira.getSpace(space)
        result = {
            'name': space.name,
            'repository': {
                'url': space.repository.url,
                'username': space.repository.username
            },
            'tags': space.tags.split(' ') if space.tags else []
        }

        return result

    @q.manage.applicationserver.expose_authenticated
    def macroConfig(self, space, page, macro, configId=None):
        return json.loads(self.alkira.getMacroConfig(space, page, macro, configId).data)

    @q.manage.applicationserver.expose_authenticated
    def updateMacroConfig(self, space, page, macro, config, configId=None):
        self.alkira.setMacroConfig(space, page, macro, config, configId)
