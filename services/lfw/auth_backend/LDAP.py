import ldap
from pylabs import q, p

class LDAPAuthService:
    def __init__(self):
        config = q.tools.inifile.open(q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname, "cfg", "auth_ldap.cfg"))
        self.config = config.getFileAsDict()
        self.hostname = self.config["LDAP"]["hostname"]
        self.port = int(self.config["LDAP"]["port"])

    def verifyUserIdentity(self, login, password):
        bind = "uid=%s,%s,%s" % (login, self.config["LDAP"]["people_rdn"], self.config["LDAP"]["base_dn"])
        conn = ldap.open(self.hostname, self.port)
        try:
            conn.simple_bind_s(bind, password)
            return True
        except:
            return False

BACKEND = LDAPAuthService
