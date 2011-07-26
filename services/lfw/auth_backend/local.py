import hashlib
from pylabs import q, p

class LocalAuthService:
    def __init__(self):
        config = q.tools.inifile.open(q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname, "cfg", "auth_local.cfg"))
        self.config = config.getFileAsDict()

    def verifyUserIdentity(self, login, password):
        if login in self.config:
            section = self.config[login]

            if "password" in section:
                md5 = hashlib.md5()
                md5.update(password)

                return section["password"] == md5.hexdigest()

        return False

BACKEND = LocalAuthService
