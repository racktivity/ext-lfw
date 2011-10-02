import os
import os.path
from pylabs import q, p
import urllib
import urllib2
import inspect
import functools
import json
import sys
from alkira import Alkira
import alkira

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

    @staticmethod
    def getAuthorizedFunctions():
        functions = []

        for funcName in dir(LFWService): # loop over functions of our class
            funcObj = getattr(LFWService, funcName)
            if getattr(funcObj, "APPLICATIONSERVER_EXPOSE_AUTHORIZED", False):
                #needs authorization
                if hasattr(funcObj, "auth_categories"):
                    functions.append(getattr(funcObj, "auth_categories"))

        return functions

    def getHeaders(self, request):
        headers = dict()
        if not isinstance(request, basestring):
            for header in request._request.requestHeaders.getAllRawHeaders():
                headers[header[0]] = header[1][0]
        return headers

    def getAuthHeaders(self, headers):
        authHeader = headers["Authorization"]
        oAuthHeaders = dict()
        for item in authHeader.split(','):
            key, value = item.split('=', 1)
            key = key.strip()
            value = value.strip('"')
            oAuthHeaders[key] = urllib2.unquote(value)
        return oAuthHeaders

    def getUsername(self, request):
        headers = self.getHeaders(request)
        if "Authorization" in headers:
            oAuthHeaders = self.getAuthHeaders(headers)
            if "oauth_consumer_key" in oAuthHeaders:
                return oAuthHeaders['oauth_consumer_key']

        return "anonymous"

    def getTokenAndUsername(self, request):
        token = None
        username = None
        headers = self.getHeaders(request)
        if "Authorization" in  headers:
            oAuthHeaders = self.getAuthHeaders(headers)
            if "oauth_consumer_key" in oAuthHeaders:
                username = oAuthHeaders["oauth_consumer_key"]
            if "oauth_token" in oAuthHeaders:
                token = oAuthHeaders["oauth_token"]

        if token and username:
            return {"token": token, "username": username}
        return None

    @q.manage.applicationserver.expose_authorized(defaultGroups=["public"], authorizeParams={"space": "space"}, authorizeRule="view page")
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

    @q.manage.applicationserver.expose_authorized(defaultGroups=["public"], authorizeParams={}, authorizeRule="view page")
    def listSpaces(self, term=None):
        return self.alkira.listSpaces()

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, authorizeRule="create space")
    def createSpace(self, name, tags="", order=None):
        self.alkira.createSpace(name, tags.split(' '), order=order)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={"space": "name"}, authorizeRule="update space")
    def updateSpace(self, name, newname=None, tags=""):
        self.alkira.updateSpace(name, newname, tags.split(' '))

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, authorizeRule="sort spaces")
    def sortSpaces(self, spaces, tags=""):
        """
        get space names in a specific order and update the actual spaces to reflect this order
        @spaces: list of spaces in the desired order
        """
        for order, space in enumerate(spaces):
            self.alkira.updateSpace(space, order=order + 1)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={"space": "name"}, authorizeRule="delete space")
    def deleteSpace(self, name):
        self.alkira.deleteSpace(name)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, authorizeRule="get user info")
    def listUsers(self, login=None):
        return self.alkira.listUsers(login)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, authorizeRule="get user info")
    def listUsersInfo(self):
        return self.alkira.listUsersInfo()

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, authorizeRule="get user info")
    def getUserInfo(self, login):
        return self.alkira._getUserInfo(login)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, authorizeRule="create user")
    def createUser(self, login, name=None, password=None, applicationserver_request=""):
        return self.alkira.createUser(login, name, password, self.getTokenAndUsername(applicationserver_request))

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, authorizeRule="delete user")
    def deleteUser(self, userguid, applicationserver_request=""):
        user = p.api.action.ui.user.getObject(userguid)
        result = self.getTokenAndUsername(applicationserver_request)
        if result['username'] == user.name:
            return False
        return self.alkira.deleteUser(userguid, result)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, authorizeRule="update user")
    def updateUser(self, userguid, name=None, password=None, applicationserver_request=""):
        return self.alkira.updateUser(userguid, name, password, self.getTokenAndUsername(applicationserver_request))

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, authorizeRule="add user to group")
    def addUserToGroup(self, userguid, groupguid, applicationserver_request=""):
        return self.alkira.addUserToGroup(userguid, groupguid, self.getTokenAndUsername(applicationserver_request))

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, authorizeRule="remove user from group")
    def removeUserFromGroup(self, userguid, groupguid, applicationserver_request=""):
        return self.alkira.removeUserFromGroup(userguid, groupguid, self.getTokenAndUsername(applicationserver_request))

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, authorizeRule="create group")
    def createGroup(self, name, applicationserver_request=""):
        return self.alkira.createGroup(name, self.getTokenAndUsername(applicationserver_request))

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, authorizeRule="delete group")
    def deleteGroup(self, groupguid, applicationserver_request=""):
        return self.alkira.deleteGroup(groupguid, self.getTokenAndUsername(applicationserver_request))

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, authorizeRule="get group info")
    def listGroups(self, name=None):
        return self.alkira.listGroups(name)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, authorizeRule="get group info")
    def getGroupInfo(self, name):
        return self.alkira._getGroupInfo(name)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["public"], authorizeParams={}, authorizeRule="get own groups")
    def getMyGroups(self, applicationserver_request=""):
        return self.alkira.getUserGroups(self.getUsername(applicationserver_request))

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, authorizeRule="update group")
    def updateGroup(self, groupguid, name):
        return self.alkira.updateGroup(groupguid, name)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, authorizeRule="get group info")
    def listGroupsInfo(self):
        return self.alkira.listGroupsInfo()

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, authorizeRule="assign rule")
    def assignRule(self, groupguids, function, context, applicationserver_request=""):
        return self.alkira.assignRule(groupguids, function, context, self.getTokenAndUsername(applicationserver_request))

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, authorizeRule="revoke rule")
    def revokeRule(self, groupguids, function, context, applicationserver_request=""):
        return self.alkira.revokeRule(groupguids, function, context, self.getTokenAndUsername(applicationserver_request))

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, authorizeRule="get group info")
    def listRulesInfo(self):
        return self.alkira.listRulesInfo()

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, authorizeRule="get group info")
    def listPossibleRules(self):
        rules = []
        spaces = filter(lambda s: s not in (alkira.ADMINSPACE, alkira.IDESPACE), self.alkira.listSpaces())

        from ide import ide
        from authservice import AuthService
        functions = LFWService.getAuthorizedFunctions()
        for func in ide.getAuthorizedFunctions():
            functions.append(func)
        for func in AuthService.getAuthorizedFunctions():
            functions.append(func)

        def addRule(rule):
            for r in rules:
                if r["function"] == rule["function"] and r["context"] == rule["context"]:
                    return
            rules.append(rule)

        for func in functions:
            if not "authorizeParams" in func:
                continue
            if not "authorizeRule" in func:
                continue

            if "space" in func["authorizeParams"]:
                for space in spaces:
                    addRule({ "function": func["authorizeRule"], "context": { "space": space} })
                #add catch all
                addRule({ "function": func["authorizeRule"], "context": {} })
            else:
                addRule({ "function": func["authorizeRule"], "context": {} })

        return rules

    @q.manage.applicationserver.expose_authorized(defaultGroups=["public"], authorizeParams={"space": "space"}, authorizeRule="view page")
    def listPages(self, space=None, term=None):
        return self.alkira.listPages(space)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["public"], authorizeParams={"space": "space"}, authorizeRule="view page")
    def countPages(self, space=None):
        return self.alkira.countPages(space=space)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["public"], authorizeParams={"space": "space"}, authorizeRule="view page")
    def categories(self, space=None, term=None):
        return self.alkira.getitems('category', space, term)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["public"], authorizeParams={}, authorizeRule="search")
    def search(self, text=None, tags=None):
        return self.alkira.search(text=text, tags=tags)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["public"], authorizeParams={"space": "space"}, authorizeRule="view page")
    def breadcrumbs(self, space, name):
        return self.alkira.breadcrumbs(space, name)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["public"], authorizeParams={"space": "space"}, authorizeRule="view page")
    def getPage(self, space, name):
        if not self.alkira.spaceExists(space) or not self.alkira.pageExists(space, name):
            return {"code": 404,
                    "error": "Page Not Found"}

        page = self.alkira.getPage(space, name)
        props = ['name', 'space', 'category', 'content', 'creationdate', 'title', 'pagetype']

        result = dict([(prop, getattr(page, prop)) for prop in props])
        result['tags'] = page.tags.split(' ') if page.tags else []

        return result

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin", "creator"], authorizeParams={"space": "space"}, authorizeRule="create page")
    def createPage(self, space, name, content, parent=None, order=None, title=None, tags="", category='portal', pagetype="md"):
        if self.alkira.pageExists(space, name):
            raise ValueError("A page with the same name already exists")
        self.alkira.createPage(space=space, name=name, content=content, parent=parent, order=order, title=title, tagsList=tags.split(" "), category=category, pagetype=pagetype)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin", "creator", "editor"], authorizeParams={"space": "space"}, authorizeRule="update page")
    def updatePage(self, space, name, content, newname=None, parent=None, order=None, title=None, tags="", category=None, pagetype=None):
        if not self.alkira.pageExists(space, name):
            raise ValueError("Page '%s' doesn't exists" % name)

        if newname and newname != name:
            if self.alkira.pageExists(space, newname):
                raise ValueError("Page '%s' already exists" % newname)

        self.alkira.updatePage(space, old_name=name, name=newname,
                               content=content, parent=parent, order=order, title=title, tagsList=tags.split(" "), category=category, pagetype=pagetype)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin", "creator"], authorizeParams={"space": "space"}, authorizeRule="delete page")
    def deletePage(self, space, name):
        self.alkira.deletePage(space, name)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["public"], authorizeParams={}, authorizeRule="view page")
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

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={"space": "space"}, authorizeRule="update space")
    def importSpace(self, space, filename, cleanImport=True):
        return self.alkira.importSpace(space, filename, cleanImport=cleanImport)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={"space": "space"}, authorizeRule="update space")
    def exportSpace(self, space, filename):
        return self.alkira.exportSpace(space, filename)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={"space": "space"}, authorizeRule="update space")
    def hgPushSpace(self, space, repository, repo_username, repo_password=None):
        return self.alkira.hgPushSpace(space, repository, repo_username, repo_password=repo_password)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={"space": "space"}, authorizeRule="update space")
    def hgPullSpace(self, space, repository, repo_username, repo_password=None, dontSync=False):
        return self.alkira.hgPullSpace(space, repository, repo_username, repo_password=repo_password, dontSync=dontSync)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={"space": "space"}, authorizeRule="update space")
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

    @q.manage.applicationserver.expose_authorized(defaultGroups=["public"], authorizeParams={"space": "space"}, authorizeRule="view page")
    def macroConfig(self, space, page, macro, configId=None, applicationserver_request=""):
        username = self.getUsername(applicationserver_request)
        return json.loads(self.alkira.getMacroConfig(space, page, macro, configId, username).data)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={"space": "space"}, authorizeRule="update page")
    def updateMacroConfig(self, space, page, macro, config, configId=None, applicationserver_request=""):
        username = self.getUsername(applicationserver_request)
        self.alkira.setMacroConfig(space, page, macro, config, configId, username)
