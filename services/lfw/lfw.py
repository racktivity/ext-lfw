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
    def spaces(self, term=None):
        return filter(lambda s: s != "Admin", self.alkira.listSpaces())
        #return self.alkira.listSpaces()

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

    @q.manage.applicationserver.expose
    def generic(self, tagstring=None, macroname=None, params=None, *args, **kwargs):
        q.logger.log('[GENERIC] Request tagstring: %s' % tagstring, 5)
        params = params or dict()
        tags = q.base.tags.getObject(tagstring)

        params['tags'] = tags
        params['service'] = self
        params.update(kwargs)
        params['args'] = args

        self._tasklet_engine.execute(params=params, tags=('pylabsmacro', macroname, ))

        result = params.get('result', '')
        q.logger.log('[GENERIC] Result: %s' % result, 5)

        return result

    @q.manage.applicationserver.expose
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

    @q.manage.applicationserver.expose
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

    @q.manage.applicationserver.expose
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

    @q.manage.applicationserver.expose
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

    @q.manage.applicationserver.expose
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
