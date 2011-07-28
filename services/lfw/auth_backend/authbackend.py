from osis.store.OsisDB import OsisDB

class AuthBackend(object):
    def __init__(self):
        super(AuthBackend, self).__init__()
        self.osis = OsisDB().getConnection(p.api.appname)

    def verifyUserIdentity(self, login, password):
        raise NotImplementedError()

    def createUsergroup(self, usergroupinfo):
        raise NotImplementedError()

    def deleteUsergroup(self, usergroupid):
        raise NotImplementedError()

    def createUser(self, userinfo):
        raise NotImplementedError()

    def addUserToGroup(self, userid, usergroupid):
        raise NotImplementedError()

    def deleteUserFromGroup(self, userid, usergroupid):
        raise NotImplementedError()

    def authorise(self, groups, functionname, context):
        raise NotImplementedError()

    def unAuthorise(self, groups,  functionname, context):
        raise NotImplementedError()

    def listAuthorisation(self, groups=None, functionname=None, context=None):
        raise NotImplementedError()

    def isAuthorised(self, groups, functionname, context):
        raise NotImplementedError()



