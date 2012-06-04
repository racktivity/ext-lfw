#pylint: disable=E1101
from osis.store.OsisDB import OsisDB
from pylabs import p, q
from racktivity import authorization
import json
from alkira.serialize import json_print_dict
from alkira.alkira import getOsisViewsMap

PUBLIC_GROUP = "Public Group"
ADMIN_GROUP = "Admins"
ANON_USER = "anonymous"
USER_GROUP = "Users"

class AuthBackend(object):
    def __init__(self):
        super(AuthBackend, self).__init__()
        self.osis = OsisDB().getConnection(p.api.appname)
        self.initChecked = False
        self.adminGroupGuid = None
        self.publicGroupGuid = None
        self.anonymousUserGuid = None
        self.userGroupGuid = None
        self.osisViewsMap = getOsisViewsMap()

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

        #make sure we have a users group
        userGroup = AuthBackend._getGroup(self, USER_GROUP)
        if not bool(userGroup):
            self.userGroupGuid = AuthBackend.createUsergroup(self, { "name": USER_GROUP })
        else:
            self.userGroupGuid = userGroup[0]

        #make sure we have an anonymous user
        self.anonymousUserGuid = AuthBackend._getUsers(self, ANON_USER)
        if not bool(self.anonymousUserGuid):
            #We are Anonymous. We are Legion. We do not forgive. We do not forget. Expect us.
            self.anonymousUserGuid = AuthBackend.createUser(self, { "login": ANON_USER, "name": "Anonymous User" })
        else:
            self.anonymousUserGuid = self.anonymousUserGuid[0]

    def _getGroup(self, name):
        searchfilter = self.osis.getFilterObject()
        groupTable = self.osisViewsMap['group']['tableName']
        searchfilter.add(groupTable, "name", name, True)
        return self.osis.objectsFind("ui", "group", searchfilter)

    def _groupExists(self, name):
        return bool(self._getGroup(name))

    def _getUsers(self, login):
        searchfilter = self.osis.getFilterObject()
        userTable = self.osisViewsMap['user']['tableName']
        searchfilter.add(userTable, "login", login, True)
        return self.osis.objectsFind("ui", "user", searchfilter)

    def _userExists(self, login):
        return bool(self._getUsers(login))

    def _getRules(self, group, functionname, context):
        searchfilter = self.osis.getFilterObject()
        authoriseruleTable = self.osisViewsMap['authoriserule']['tableName']
        searchfilter.add(authoriseruleTable, "groupguids", ";" + group + ";", False)
        searchfilter.add(authoriseruleTable, "function", functionname, True)
        searchfilter.add(authoriseruleTable, "context", json_print_dict(context), True)
        return self.osis.objectsFind("ui", "authoriserule", searchfilter)

    def _ruleExists(self, group, functionname, context):
        return bool(self._getRules(group, functionname, context))

    def verifyUserIdentity(self, login, password): #pylint: disable=W0613
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
        userTable = self.osisViewsMap['user']['tableName']
        searchfilter.add(userTable, "groupguids", ";" + usergroupid + ";", False)
        userguids = self.osis.objectsFind("ui", "user", searchfilter)
        for userguid in userguids:
            user = p.api.model.ui.user.get(userguid)
            user.groups.remove(usergroupid)
            p.api.model.ui.user.save(user)

        #make sure rules don't reference the group anymore
        searchfilter = self.osis.getFilterObject()
        authoriseruleTable = self.osisViewsMap['authoriserule']['tableName']
        searchfilter.add(authoriseruleTable, "groupguids", ";" + usergroupid + ";", False)
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
            # Keep anonymous out of users group, they can't be trusted...
            if userinfo["login"] != ANON_USER:
                user.groups.append(self.userGroupGuid)
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

    def listAuthorisation(self, groups=None, functionname=None, context=None): #pylint: disable=W0613
        self._initCheck()
        q.errorconditionhandler.raiseError("Not implemented")

    def isAuthorised(self, groups, functionname, context):
        q.logger.log("Checking if group %s is authorized for function '%s' with context '%s' " % (str(groups), functionname, str(context)), 3)
        self._initCheck()
        if not isinstance(groups, list):
            groups = [ groups ]
        def doSearch(groupguid, functionname, context):
            searchfilter = self.osis.getFilterObject()
            authoriseruleTable = self.osisViewsMap['authoriserule']['tableName']
            searchfilter.add(authoriseruleTable, "groupguids", ";" + groupguid + ";", False)
            searchfilter.add(authoriseruleTable, "function", functionname, True)
            rules = self.osis.objectsFindAsView("ui", "authoriserule", searchfilter, authoriseruleTable)
            # No rules found
            if not rules:
                q.logger.log("No rules found for group %s" % (str(groups)), 3)
                return False

            for rule in rules:
                ruleContext = json.loads(rule['context'])
                # Remove the '_rulegroup' and '_forceinheritance' items from the saved context.
                # This is only used to map stored rules to rulegroups in the UI
                # And yes, I know it's dirty
                if authorization.RacktivityAuthorization.RULE_GROUP_PARAM in ruleContext:
                    ruleContext.pop(authorization.RacktivityAuthorization.RULE_GROUP_PARAM)
                if authorization.RacktivityAuthorization.FORCE_INHERITANCE_PARAM in ruleContext:
                    ruleContext.pop(authorization.RacktivityAuthorization.FORCE_INHERITANCE_PARAM)

                ruleMatch = True
                contextKeys = set(context.keys())
                ruleContextKeys = set(ruleContext.keys())

                if not ruleContextKeys.issubset(contextKeys):
                    q.logger.log("Context keys do not match for rule %s" % (str(rule)), 3)
                    ruleMatch = False
                else:
                    for key, value in context.iteritems():
                        keyMatches = True
                        if key in ruleContext and not (value == ""):
                            valueToMatch = ruleContext[key]
                            if isinstance(value, dict):
                                valueToMatch = json.loads(valueToMatch)
                                if set(valueToMatch.keys()).issubset(set(value.keys())):
                                    for valueKey in value.keys():
                                        if not valueKey in valueToMatch:
                                            continue
                                        if not (value[valueKey] == valueToMatch[valueKey]):
                                            keyMatches = False
                                else:
                                    keyMatches = False
                            elif isinstance(value, list):
                                if valueToMatch not in set(value):
                                    keyMatches = False
                            elif not (value == valueToMatch):
                                keyMatches = False
                        if not keyMatches:
                            q.logger.log("'%s' not in '%s' or '%s' != '%s'" % (key, str(ruleContext), value, valueToMatch), 3)
                            ruleMatch = False
                            break
                    if ruleMatch:
                        return True
            return False

        for groupguid in groups:
            if not groupguid:
                continue

            if doSearch(groupguid, functionname, context):
                return True

        return False
