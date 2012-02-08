import hashlib, authbackend
from pylabs import q, p

class LocalAuthBackend(authbackend.AuthBackend):
    def __init__(self):
        super(LocalAuthBackend, self).__init__()
        self.config = q.tools.inifile.open(q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname, "cfg", \
            "auth_local.cfg"))

    def verifyUserIdentity(self, login, password):
        if self.config.checkSection(login) and self.config.checkParam(login, "password"):
            md5 = hashlib.md5()
            md5.update(str(password))

            return self.config.getValue(login, "password") == md5.hexdigest()

        return False

    def createUser(self, userinfo):
        if self.config.checkSection(userinfo["login"]):
            q.errorconditionhandler.raiseError("User %s already exists in the backend." % userinfo["login"])

        md5 = hashlib.md5()
        md5.update(str(userinfo["password"]))

        self.config.addSection(userinfo["login"])
        self.config.addParam(userinfo["login"], "password", md5.hexdigest())
        self.config.write()

        return super(LocalAuthBackend, self).createUser(userinfo)

    def deleteUser(self, userid):
        login = super(LocalAuthBackend, self).deleteUser(userid)
        if not self.config.checkSection(login):
            q.errorconditionhandler.raiseError("User %s does not exists in the backend." % login)

        self.config.removeSection(login)
        self.config.write()
        return True

    def updateUser(self, userid, userinfo):
        login = super(LocalAuthBackend, self).updateUser(userid, userinfo)
        if not self.config.checkSection(login):
            q.errorconditionhandler.raiseError("User %s does not exists in the backend." % login)

        if "password" in userinfo:
            md5 = hashlib.md5()
            md5.update(userinfo["password"])
            self.config.setParam(login, "password", md5.hexdigest())
        return True

BACKEND = LocalAuthBackend
