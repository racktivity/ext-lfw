from osis.store.OsisDB import OsisDB
from pylabs import p, q
import json

PUBLIC_GROUP = "Public Group"
ADMIN_GROUP = "Admins"
ANON_USER = "anonymous"

class AuthBackend(object):
    def __init__(self):
        super(AuthBackend, self).__init__()
        self.osis = OsisDB().getConnection(p.api.appname)
        self.initChecked = False
        self.adminGroupGuid = None
        self.publicGroupGuid = None
        self.anonymousUserGuid = None

    def _initCheck(self):
        if self.initChecked:
            return

        self.initChecked = True

        #make sure we have an admins group
        adminGroup = AuthBackend._getGroup(self, ADMIN_GROUP)
        if not bool(adminGroup):
            self.adminGroupGuid = AuthBackend.createUsergroup(self, { "name": ADMIN_GROUP })
        else:
            self.adminGroupGuid = adminGroup[0]

        #make sure we have a public group
        publicGroup = AuthBackend._getGroup(self, PUBLIC_GROUP)
        if not bool(publicGroup):
            self.publicGroupGuid = AuthBackend.createUsergroup(self, { "name": PUBLIC_GROUP })
        else:
            self.publicGroupGuid = publicGroup[0]

        #make sure we have an anonymous user
        self.anonymousUserGuid = AuthBackend._getUsers(self, ANON_USER)
        if not bool(self.anonymousUserGuid):
            #We are Anonymous. We are Legion. We do not forgive. We do not forget. Expect us.
            self.anonymousUserGuid = AuthBackend.createUser(self, { "login": ANON_USER, "name": "Anonymous User" })
        else:
            self.anonymousUserGuid = self.anonymousUserGuid[0]

    def _getGroup(self, name):
        searchfilter = self.osis.getFilterObject()
        searchfilter.add("ui_view_group_list", "name", name, True)
        return self.osis.objectsFind("ui", "group", searchfilter)

    def _groupExists(self, name):
        return bool(self._getGroup(name))

    def _getUsers(self, login):
        searchfilter = self.osis.getFilterObject()
        searchfilter.add("ui_view_user_list", "login", login, True)
        return self.osis.objectsFind("ui", "user", searchfilter)

    def _userExists(self, login):
        return bool(self._getUsers(login))

    def _getRules(self, group, functionname, context):
        searchfilter = self.osis.getFilterObject()
        searchfilter.add("ui_view_authoriserule_list", "groupguids", ";" + group + ";", False)
        searchfilter.add("ui_view_authoriserule_list", "function", functionname, True)
        searchfilter.add("ui_view_authoriserule_list", "context", json.dumps(context), True)
        return self.osis.objectsFind("ui", "authoriserule", searchfilter)

    def _ruleExists(self, group, functionname, context):
        return bool(self._getRules(group, functionname, context))

    def verifyUserIdentity(self, login, password):
        self._initCheck()
        q.errorconditionhandler.raiseError("Not implemented")

    def createUsergroup(self, usergroupinfo):
        self._initCheck()
        if self._groupExists(usergroupinfo["name"]):
            q.errorconditionhandler.raiseError("Group %s already exists." % usergroupinfo["name"])
        else:
            group = p.api.model.ui.group.new()
            group.name = usergroupinfo["name"]
            p.api.model.ui.group.save(group)
            return group.guid

    def deleteUsergroup(self, usergroupid):
        self._initCheck()
        if usergroupid in (self.publicGroupGuid, self.adminGroupGuid):
            q.errorconditionhandler.raiseError("Unable to delete %s." % PUBLIC_GROUP)

        #make sure users don't reference the group anymore
        searchfilter = self.osis.getFilterObject()
        searchfilter.add("ui_view_user_list", "groupguids", ";" + usergroupid + ";", False)
        userguids = self.osis.objectsFind("ui", "user", searchfilter)
        for userguid in userguids:
            user = p.api.model.ui.user.get(userguid)
            user.groups.remove(usergroupid)
            p.api.model.ui.user.save(user)

        #make sure rules don't reference the group anymore
        searchfilter = self.osis.getFilterObject()
        searchfilter.add("ui_view_authoriserule_list", "groupguids", ";" + usergroupid + ";", False)
        ruleguids = self.osis.objectsFind("ui", "authoriserule", searchfilter)
        for ruleguid in ruleguids:
            rule = p.api.model.ui.authoriserule.get(ruleguid)
            rule.groupguids.remove(usergroupid)
            if not len(rule.groupguids):
                p.api.model.ui.authoriserule.delete(ruleguid)
            else:
                p.api.model.ui.authoriserule.save(rule)

        p.api.model.ui.group.delete(usergroupid)
        return True

    def createUser(self, userinfo):
        self._initCheck()
        if self._userExists(userinfo["login"]):
            q.errorconditionhandler.raiseError("User %s already exists." % userinfo["login"])
        else:
            user = p.api.model.ui.user.new()
            user.login = userinfo["login"]
            if "name" in userinfo:
                user.name = userinfo["name"]
            user.groups.append(self.publicGroupGuid)
            p.api.model.ui.user.save(user)
            return user.guid

    def deleteUser(self, userid):
        self._initCheck()
        if userid == self.anonymousUserGuid:
            q.errorconditionhandler.raiseError("Unable to delete %s." % ANON_USER)
        login = p.api.model.ui.user.get(userid).login
        p.api.model.ui.user.delete(userid)
        return login

    def updateUser(self, userid, userinfo):
        self._initCheck()
        user = p.api.model.ui.user.get(userid)
        if "name" in userinfo:
            user.name = userinfo["name"]
        p.api.model.ui.user.save(user)
        return user.login

    def addUserToGroup(self, userid, usergroupid):
        self._initCheck()
        user = p.api.model.ui.user.get(userid)
        if usergroupid in user.groups:
            q.errorconditionhandler.raiseError("User is already in that group.")

        user.groups.append(usergroupid)
        p.api.model.ui.user.save(user)
        return True

    def deleteUserFromGroup(self, userid, usergroupid):
        self._initCheck()
        user = p.api.model.ui.user.get(userid)
        if not usergroupid in user.groups:
            q.errorconditionhandler.raiseError("User is not in that group.")

        user.groups.remove(usergroupid)
        p.api.model.ui.user.save(user)
        return True

    def authorise(self, groups, functionname, context):
        self._initCheck()
        if not isinstance(groups, list):
            groups = [ groups ]
        for group in groups:
            if self._ruleExists(group, functionname, context):
                q.errorconditionhandler.raiseError("Rule already exists.")

        rule = p.api.model.ui.authoriserule.new()
        rule.groupguids = groups
        rule.function = functionname
        rule.context = context
        p.api.model.ui.authoriserule.save(rule)
        return rule.guid

    def unAuthorise(self, groups, functionname, context):
        self._initCheck()
        if not isinstance(groups, list):
            groups = [ groups ]
        found = False
        for group in groups:
            rules = self._getRules(group, functionname, context)
            for rule in rules:
                p.api.model.ui.authoriserule.delete(rule)
                found = True
        return found

    def listAuthorisation(self, groups=None, functionname=None, context=None):
        self._initCheck()
        q.errorconditionhandler.raiseError("Not implemented")

    def isAuthorised(self, groups, functionname, context):
        self._initCheck()
        if not isinstance(groups, list):
            groups = [ groups ]
        def doSearch(groupguid, functionname, context):
            searchfilter = self.osis.getFilterObject()
            searchfilter.add("ui_view_authoriserule_list", "groupguids", ";" + groupguid + ";", False)
            searchfilter.add("ui_view_authoriserule_list", "function", functionname, True)
            searchfilter.add("ui_view_authoriserule_list", "context", json.dumps(context), True)
            return bool(self.osis.objectsFind("ui", "authoriserule", searchfilter))

        for groupguid in groups:
            if not groupguid:
                continue

            if doSearch(groupguid, functionname, context):
                return True

            #add an aditional search for catch all context if context isn't already catch all
            if context:
                if doSearch(groupguid, functionname, {}):
                    return True
        return False
