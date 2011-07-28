import sys, os
from pylabs import q, p
from actionservice import ActionService

class AuthService(ActionService):
    def __init__(self):
        config = q.tools.inifile.open(q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname, "cfg", "auth.cfg"))

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "auth_backend"))

        #load backend
        backend = __import__(config.getValue("auth", "backend"), level=1)
        self.backend = getattr(backend, "BACKEND")()

    @q.manage.applicationserver.expose
    def verifyUserIdentity(self, login, password):
        return self.backend.verifyUserIdentity(login, password)

    @q.manage.applicationserver.expose_authenticated
    def createUsergroup(self, usergroupinfo):
        return self.backend.createUsergroup(usergroupinfo)

    @q.manage.applicationserver.expose_authenticated
    def deleteUsergroup(self, usergroupid):
        return self.backend.deleteUsergroup(usergroupid)

    @q.manage.applicationserver.expose_authenticated
    def createUser(self, userinfo):
        return self.backend.createUser(userinfo)

    @q.manage.applicationserver.expose_authenticated
    def addUserToGroup(self, userid, usergroupid):
        return self.backend.addUserToGroup(userid, usergroupid)

    @q.manage.applicationserver.expose_authenticated
    def deleteUserFromGroup(self, userid, usergroupid):
        return self.backend.deleteUserFromGroup(groups, userid, usergroupid)

    @q.manage.applicationserver.expose_authenticated
    def authorise(self, groups, functionname, context):
        return self.backend.authorise(groups, functionname, context)

    @q.manage.applicationserver.expose_authenticated
    def unAuthorise(self, groups,  functionname, context):
        return self.backend.unAuthorise(groups, functionname, context)

    @q.manage.applicationserver.expose_authenticated
    def listAuthorisation(self, groups=None, functionname=None, context=None):
        return self.backend.listAuthorisation(groups, functionname, context)

    @q.manage.applicationserver.expose_authenticated
    def isAuthorised(self, groups, functionname, context):
        return self.backend.isAuthorised(groups, functionname, context)
