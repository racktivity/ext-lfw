import sys, os
from pylabs import q, p

class AuthService(object):
    def __init__(self):
        config = q.tools.inifile.open(q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname, "cfg", "auth.cfg"))

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "auth_backend"))

        #load backend
        backend = __import__(config.getValue("auth", "backend"), level=1)
        self.backend = getattr(backend, "BACKEND")()

    @q.manage.applicationserver.expose
    def verifyUserIdentity(self, login, password):
        return self.backend.verifyUserIdentity(login, password)

