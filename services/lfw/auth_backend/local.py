import hashlib, authbackend
from pylabs import q, p

def reload_config(func):

    def wrapper(*args, **kwargs):
        args[0]._reloadConfig() #pylint: disable=W0212
        return func(*args, **kwargs)

    return wrapper

class LocalAuthBackend(authbackend.AuthBackend):
    def __init__(self):
        super(LocalAuthBackend, self).__init__()
        self.config = None
        self._reloadConfig()

    def _reloadConfig(self):
        self.config = q.tools.inifile.open(q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname, "cfg", \
            "auth_local.cfg"))

    @reload_config
    def verifyUserIdentity(self, login, password):
        if self.config.checkSection(login) and self.config.checkParam(login, "password"):
            md5 = hashlib.md5()
            md5.update(str(password))

            return self.config.getValue(login, "password") == md5.hexdigest()

        return False

    @reload_config
    def createUser(self, userinfo):
        if self.config.checkSection(userinfo["login"]):
            q.errorconditionhandler.raiseError("User %s already exists in the backend." % userinfo["login"])

        md5 = hashlib.md5()
        md5.update(str(userinfo["password"]))

        self.config.addSection(userinfo["login"])
        self.config.addParam(userinfo["login"], "password", md5.hexdigest())
        self.config.write()

        return super(LocalAuthBackend, self).createUser(userinfo)

    @reload_config
    def deleteUser(self, userid):
        login = super(LocalAuthBackend, self).deleteUser(userid)
        if not self.config.checkSection(login):
            q.errorconditionhandler.raiseError("User %s does not exists in the backend." % login)

        self.config.removeSection(login)
        self.config.write()
        return True

    @reload_config
    def updateUser(self, userid, userinfo):
        login = super(LocalAuthBackend, self).updateUser(userid, userinfo)
        if not self.config.checkSection(login):
            q.errorconditionhandler.raiseError("User %s does not exists in the backend." % login)

        if "password" in userinfo:
            md5 = hashlib.md5()
            md5.update(str(userinfo["password"]))
            self.config.setParam(login, "password", md5.hexdigest())
        return True

BACKEND = LocalAuthBackend
