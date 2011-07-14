import os
import os.path
from pylabs import q, p
import urllib
import urllib2
import inspect
import functools
import json
from . import Alkira

# @TODO: use sqlalchemy to construct queries - escape values
# @TODO: add space to filter criteria



class LFWService(object):

    def __init__(self):
        # Initialize API
        self.connection = p.api.model.ui
        self.alkira = Alkira(p.api)
        
        tasklet_path = q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname, 'impl', 'portal')
        self._tasklet_engine = q.taskletengine.get(tasklet_path)
        self._tasklet_engine.addFromPath(os.path.join(q.dirs.baseDir,'lib','python','site-packages','alkira', 'tasklets'))
        self.db_config_path = q.system.fs.joinPaths(q.dirs.cfgDir, 'qconfig', 'dbconnections.cfg')

    @q.manage.applicationserver.expose_authenticated
    def tags(self, space=None, term=None):
        results = self.alkira.getitems('tags', space=space, term=term)
        final_result = set()
        for item in results:
            tags = item.split(' ')
            for tag in tags:
                if term in tag:
                    final_result.add((tag.strip(',')))
        result = list(final_result)
        return result

    @q.manage.applicationserver.expose_authenticated
    def listSpaces(self, term=None):
        return self.alkira.listSpaces()

    @q.manage.applicationserver.expose_authenticated
    def createSpace(self, name, tags="", order=None):
        self.alkira.createSpace(name, tags.split(' '), order=order)

    @q.manage.applicationserver.expose
    def updateSpace(self, name, newname=None, tags=""):
        self.alkira.updateSpace(name, newname, tags.split(' '))
    
    @q.manage.applicationserver.expose
    def sortSpaces(self, spaces, tags=""):
        """
        get space names in a specific order and update the actual spaces to reflect this order
        @spaces: list of spaces in the desired order
        """
        for order, space in enumerate(spaces):
            self.alkira.updateSpace(space, order=order + 1)
    
    @q.manage.applicationserver.expose_authenticated
    def deleteSpace(self, name):
        self.alkira.deleteSpace(name)

    @q.manage.applicationserver.expose_authenticated
    def listUsers(self, username=None):
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
    def listPages(self, space=None, term=None):
        return self.alkira.listPages(space)

    @q.manage.applicationserver.expose_authenticated
    def countPages(self, space=None):
        return self.alkira.countPages(space=space)
    
    @q.manage.applicationserver.expose_authenticated
    def categories(self, space=None, term=None):
        return self.alkira.getitems('category', space, term)

    @q.manage.applicationserver.expose_authenticated
    def search(self, text=None, space=None, category=None, tags=None):
        return self.alkira.search(text=text, space=space, category=category, tags=tags)

    @q.manage.applicationserver.expose_authenticated
    def breadcrumbs(self, space, name):
        return self.alkira.breadcrumbs(space, name)

    @q.manage.applicationserver.expose_authenticated
    def getPage(self, space, name):
        if not self.alkira.spaceExists(space) or not self.alkira.pageExists(space, name):
            return {"code": 404,
                    "error": "Page Not Found"}

        page = self.alkira.getPage(space, name)
        props = ['name', 'space', 'category', 'content', 'creationdate', 'title', 'pagetype']

        result = dict([(prop, getattr(page, prop)) for prop in props])
        result['tags'] = page.tags.split(' ') if page.tags else []

        return result
    
    @q.manage.applicationserver.expose_authenticated
    def createPage(self, space, name, content, parent=None, order=None, title=None, tags="", category='portal', pagetype="md"):
        if self.alkira.pageExists(space, name):
            raise ValueError("A page with the same name already exists")
        self.alkira.createPage(space=space, name=name, content=content, parent=parent, order=order, title=title, tagsList=tags.split(" "), category=category, pagetype=pagetype)

    @q.manage.applicationserver.expose_authenticated
    def updatePage(self, space, name, content, newname=None, parent=None, order=None, title=None, tags="", category=None, pagetype=None):
        if not self.alkira.pageExists(space, name):
            raise ValueError("Page '%s' doesn't exists" % name)

        if newname and newname != name:
            if self.alkira.pageExists(space, newname):
                raise ValueError("Page '%s' already exists" % newname)

        self.alkira.updatePage(space, old_name=name, name=newname,
                               content=content, parent=parent, order=order, title=title, tagsList=tags.split(" "), category=category, pagetype=pagetype)

    @q.manage.applicationserver.expose_authenticated
    def deletePage(self, space, name):
        self.alkira.deletePage(space, name)

    @q.manage.applicationserver.expose_authenticated
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

    @q.manage.applicationserver.expose_authenticated
    def importSpace(self, space, filename, cleanImport=True):
        return self.alkira.importSpace(space, filename, cleanImport=cleanImport)

    @q.manage.applicationserver.expose_authenticated
    def exportSpace(self, space, filename):
        return self.alkira.exportSpace(space, filename)

    @q.manage.applicationserver.expose_authenticated
    def hgPushSpace(self, space, repository, repo_username, repo_password=None):
        return self.alkira.hgPushSpace(space, repository, repo_username, repo_password=repo_password)

    @q.manage.applicationserver.expose_authenticated
    def hgPullSpace(self, space, repository, repo_username, repo_password=None, dontSync=False):
        return self.alkira.hgPullSpace(space, repository, repo_username, repo_password=repo_password, dontSync=dontSync)

    @q.manage.applicationserver.expose_authenticated
    def getSpace(self, space):
        if not self.alkira.spaceExists(space):
            return {"code": 404,
                    "error": "Space Not Found"}

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

    def getHeaders(self, request):
        headers = dict()
        for header in request._request.requestHeaders.getAllRawHeaders():
            headers[header[0]] = header[1][0]
        q.logger.log("HEADERS "+ str(headers), 4)
        return headers

    def getAuthHeaders(self, headers):
        authHeader = headers["Authorization"]
        oAuthHeaders = dict()
        for item in authHeader.split(','):
            key, value = item.split('=', 1)
            key = key.strip()
            value = value.strip('"')
            oAuthHeaders[key] = urllib2.unquote(value)
        q.logger.log("OAUTH HEADERS "+ str(oAuthHeaders), 4)
        return oAuthHeaders

    def getUsername(self, request):
        headers = self.getHeaders(request)
        if "Authorization" in headers:
            oAuthHeaders = self.getAuthHeaders(headers)
            if "oauth_consumer_key" in oAuthHeaders:
                return oAuthHeaders['oauth_consumer_key']

        return None

    @q.manage.applicationserver.expose_authenticated
    def macroConfig(self, space, page, macro, configId=None, applicationserver_request=""):
        username = self.getUsername(applicationserver_request)
        return json.loads(self.alkira.getMacroConfig(space, page, macro, configId, username).data)

    @q.manage.applicationserver.expose_authenticated
    def updateMacroConfig(self, space, page, macro, config, configId=None, applicationserver_request=""):
        username = self.getUsername(applicationserver_request)
        self.alkira.setMacroConfig(space, page, macro, config, configId, username)
