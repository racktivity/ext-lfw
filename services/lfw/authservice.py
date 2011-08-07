import sys, os
from pylabs import q, p

class AuthService(object):
    def __init__(self):
        basedir = os.path.join(q.dirs.pyAppsDir, p.api.appname)
        self._authenticate = q.taskletengine.get(os.path.join(basedir, 'impl', 'authenticate'))
        self._authorize = q.taskletengine.get(os.path.join(basedir, 'impl', 'authorize'))

        config = q.tools.inifile.open(q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname, "cfg", "auth.cfg"))

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "auth_backend"))

        #load backend
        backend = __import__(config.getValue("auth", "backend"), level=1)
        self.backend = getattr(backend, "BACKEND")()

    @staticmethod
    def getAuthorizedFunctions():
        functions = []

        for funcName in dir(AuthService): # loop over functions of our class
            funcObj = getattr(AuthService, funcName)
            if getattr(funcObj, "APPLICATIONSERVER_EXPOSE_AUTHORIZED", False):
                #needs authorization
                if hasattr(funcObj, "auth_categories"):
                    functions.append(getattr(funcObj, "auth_categories"))

        return functions

    def checkAuthentication(self, request, domain, service, methodname, args, kwargs):
        q.logger.log("HEADERS from AuthService.checkAuthentication %s" % str(request._request.requestHeaders))
        tags = ('authenticate',)
        params = dict()
        params['request'] = request
        params['domain'] = domain
        params['service'] = service
        params['methodname'] = methodname
        params['args'] = args
        params['kwargs'] = kwargs
        params['result'] = True
        self._authenticate.execute(params, tags=tags)
        return params.get('result', False)

    def checkAuthorization(self, criteria, request, domain, service, methodname, args, kwargs):
        tags = ('authorize',)
        params = dict()
        params['criteria'] = criteria
        params['request'] = request
        params['domain'] = domain
        params['service'] = service
        params['methodname'] = methodname
        params['args'] = args
        params['kwargs'] = kwargs
        params['result'] = True
        self._authorize.execute(params, tags=tags)
        return params.get('result', False)

    @q.manage.applicationserver.expose
    def verifyUserIdentity(self, login, password):
        return self.backend.verifyUserIdentity(login, password)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, \
        authorizeRule="create group")
    def createUsergroup(self, usergroupinfo):
        return self.backend.createUsergroup(usergroupinfo)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, \
        authorizeRule="delete group")
    def deleteUsergroup(self, usergroupid):
        return self.backend.deleteUsergroup(usergroupid)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, \
        authorizeRule="create user")
    def createUser(self, userinfo):
        return self.backend.createUser(userinfo)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, \
        authorizeRule="delete user")
    def deleteUser(self, userid):
        return self.backend.deleteUser(userid)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, \
        authorizeRule="update user")
    def updateUser(self, userid, userinfo):
        return self.backend.updateUser(userid, userinfo)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, \
        authorizeRule="add user to group")
    def addUserToGroup(self, userid, usergroupid):
        return self.backend.addUserToGroup(userid, usergroupid)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, \
        authorizeRule="remove user from group")
    def deleteUserFromGroup(self, userid, usergroupid):
        return self.backend.deleteUserFromGroup(userid, usergroupid)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, \
        authorizeRule="assign rule")
    def authorise(self, groups, functionname, context):
        return self.backend.authorise(groups, functionname, context)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, \
        authorizeRule="revoke rule")
    def unAuthorise(self, groups, functionname, context):
        return self.backend.unAuthorise(groups, functionname, context)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={}, \
        authorizeRule="assign rule")
    def listAuthorisation(self, groups=None, functionname=None, context=None):
        return self.backend.listAuthorisation(groups, functionname, context)

    @q.manage.applicationserver.expose_authenticated
    def isAuthorised(self, groups, functionname, context):
        return self.backend.isAuthorised(groups, functionname, context)
