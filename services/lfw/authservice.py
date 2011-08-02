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

    @q.manage.applicationserver.expose_authorized()
    def createUsergroup(self, usergroupinfo):
        return self.backend.createUsergroup(usergroupinfo)

    @q.manage.applicationserver.expose_authorized()
    def deleteUsergroup(self, usergroupid):
        return self.backend.deleteUsergroup(usergroupid)

    @q.manage.applicationserver.expose_authorized()
    def createUser(self, userinfo):
        return self.backend.createUser(userinfo)

    @q.manage.applicationserver.expose_authorized()
    def deleteUser(self, userid):
        return self.backend.deleteUser(userid)

    @q.manage.applicationserver.expose_authorized()
    def updateUser(self, userid, userinfo):
        return self.backend.updateUser(userid, userinfo)

    @q.manage.applicationserver.expose_authorized()
    def addUserToGroup(self, userid, usergroupid):
        return self.backend.addUserToGroup(userid, usergroupid)

    @q.manage.applicationserver.expose_authorized()
    def deleteUserFromGroup(self, userid, usergroupid):
        return self.backend.deleteUserFromGroup(userid, usergroupid)

    @q.manage.applicationserver.expose_authorized()
    def authorise(self, groups, functionname, context):
        return self.backend.authorise(groups, functionname, context)

    @q.manage.applicationserver.expose_authorized()
    def unAuthorise(self, groups,  functionname, context):
        return self.backend.unAuthorise(groups, functionname, context)

    @q.manage.applicationserver.expose_authorized()
    def listAuthorisation(self, groups=None, functionname=None, context=None):
        return self.backend.listAuthorisation(groups, functionname, context)

    @q.manage.applicationserver.expose_authorized()
    def isAuthorised(self, groups, functionname, context):
        return self.backend.isAuthorised(groups, functionname, context)
