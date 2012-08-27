from osis.store.OsisDB import OsisDB
from pylabs import p, q
try:
    from racktivity import authorization
except ImportError:
    authorization = None
try:
    from racktivity.cache import cache
except ImportError:
    cache = None
import json
from alkira.serialize import json_print_dict

PUBLIC_GROUP = "Public Group"
ADMIN_GROUP = "Admins"
ANON_USER = "anonymous"
USER_GROUP = "Users"

def ensure_groups(func):

    def wrapper(*args, **kwargs):
        args[0]._initCheck() #pylint: disable=W0212
        return func(*args, **kwargs)

    return wrapper

class AuthBackend(object):
    def __init__(self):
        super(AuthBackend, self).__init__()
        self.osis = OsisDB().getConnection(p.api.appname)
        self.initChecked = False
        self.adminGroupGuid = None
        self.publicGroupGuid = None
        self.anonymousUserGuid = None
        self.userGroupGuid = None
        self._cache = cache.getApi() if cache else None
        self._cacheHash = cache.calculateHash({ "__name__": "authorization_authbackend" }) if cache else None

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
        searchfilter.add('group', "name", name, True)
        return self.osis.objectsFind("ui", "group", searchfilter)

    def _groupExists(self, name):
        return bool(self._getGroup(name))

    def _getUsers(self, login):
        searchfilter = self.osis.getFilterObject()
        searchfilter.add('user', "login", login, True)
        return self.osis.objectsFind("ui", "user", searchfilter)

    def _userExists(self, login):
        return bool(self._getUsers(login))

    def _getRules(self, group, functionname, context):
        searchfilter = self.osis.getFilterObject()
        searchfilter.add('authoriserule', "groupguids", ";" + group + ";", False)
        searchfilter.add('authoriserule', "function", functionname, True)
        searchfilter.add('authoriserule', "context", json_print_dict(context), True)
        return self.osis.objectsFind("ui", "authoriserule", searchfilter)

    def _ruleExists(self, group, functionname, context):
        return bool(self._getRules(group, functionname, context))

    def _getCachedIsAuhtorised(self, groups, functionname, context):
        if not self._cache:
            return None

        #get main authorization dict
        results = self._cache.get(self._cacheHash) or {}

        #calculate hash for isAuthorised
        isAuthorisedHash = cache.calculateHash({ "groups": groups, "functionname": functionname, "context": context })
        if isAuthorisedHash in results: #get the cached result
            return results[isAuthorisedHash]

        return None

    def _setCachedIsAuthorized(self, groups, functionname, context, value):
        if not self._cache:
            return

        #get main authorization dict
        results = self._cache.get(self._cacheHash) or {}

        #calculate hash for isAuthorised
        isAuthorisedHash = cache.calculateHash({ "groups": groups, "functionname": functionname, "context": context })
        results[isAuthorisedHash] = value

        #save main authorization dict
        self._cache.set(self._cacheHash, results, cache.maxduration)

    def _clearCache(self):
        if not self._cache:
            return

        #clear main authorization dict
        self._cache.flushByKeys([ self._cacheHash ])

    @ensure_groups
    def verifyUserIdentity(self, login, password): #pylint: disable=W0613
        q.errorconditionhandler.raiseError("Not implemented")

    @ensure_groups
    def createUsergroup(self, usergroupinfo):
        if self._groupExists(usergroupinfo["name"]):
            q.errorconditionhandler.raiseError("Group %s already exists." % usergroupinfo["name"])
        else:
            group = p.api.model.ui.group.new()
            group.name = usergroupinfo["name"]
            p.api.model.ui.group.save(group)
            return group.guid

    @ensure_groups
    def deleteUsergroup(self, usergroupid):
        if usergroupid in (self.publicGroupGuid, self.adminGroupGuid):
            q.errorconditionhandler.raiseError("Unable to delete %s." % PUBLIC_GROUP)

        #make sure users don't reference the group anymore
        searchfilter = self.osis.getFilterObject()
        searchfilter.add('user', "groupguids", ";" + usergroupid + ";", False)
        userguids = self.osis.objectsFind("ui", "user", searchfilter)
        for userguid in userguids:
            user = p.api.model.ui.user.get(userguid)
            user.groups.remove(usergroupid)
            p.api.model.ui.user.save(user)

        #make sure rules don't reference the group anymore
        searchfilter = self.osis.getFilterObject()
        searchfilter.add('authoriserule', "groupguids", ";" + usergroupid + ";", False)
        ruleguids = self.osis.objectsFind("ui", "authoriserule", searchfilter)
        for ruleguid in ruleguids:
            rule = p.api.model.ui.authoriserule.get(ruleguid)
            rule.groupguids.remove(usergroupid)
            if not len(rule.groupguids):
                p.api.model.ui.authoriserule.delete(ruleguid)
            else:
                p.api.model.ui.authoriserule.save(rule)

        p.api.model.ui.group.delete(usergroupid)

        #clear authorization cache
        self._clearCache()

        return True

    @ensure_groups
    def createUser(self, userinfo):
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

    @ensure_groups
    def deleteUser(self, userid):
        if userid == self.anonymousUserGuid:
            q.errorconditionhandler.raiseError("Unable to delete %s." % ANON_USER)
        login = p.api.model.ui.user.get(userid).login
        p.api.model.ui.user.delete(userid)
        return login

    @ensure_groups
    def updateUser(self, userid, userinfo):
        user = p.api.model.ui.user.get(userid)
        if "name" in userinfo:
            user.name = userinfo["name"]
        p.api.model.ui.user.save(user)
        return user.login

    @ensure_groups
    def addUserToGroup(self, userid, usergroupid):
        user = p.api.model.ui.user.get(userid)
        if usergroupid in user.groups:
            q.errorconditionhandler.raiseError("User is already in that group.")

        user.groups.append(usergroupid)
        p.api.model.ui.user.save(user)
        return True

    @ensure_groups
    def deleteUserFromGroup(self, userid, usergroupid):
        user = p.api.model.ui.user.get(userid)
        if not usergroupid in user.groups:
            q.errorconditionhandler.raiseError("User is not in that group.")

        user.groups.remove(usergroupid)
        p.api.model.ui.user.save(user)
        return True

    @ensure_groups
    def authorise(self, groups, functionname, context):
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

        #clear authorization cache
        self._clearCache()

        return rule.guid

    @ensure_groups
    def unAuthorise(self, groups, functionname, context):
        if not isinstance(groups, list):
            groups = [ groups ]
        found = False
        for group in groups:
            rules = self._getRules(group, functionname, context)
            for rule in rules:
                p.api.model.ui.authoriserule.delete(rule)
                found = True

        if found:
            #clear authorization cache
            self._clearCache()

        return found

    @ensure_groups
    def listAuthorisation(self, groups=None, functionname=None, context=None): #pylint: disable=W0613
        q.errorconditionhandler.raiseError("Not implemented")

    @ensure_groups
    def isAuthorised(self, groups, functionname, context):
        q.logger.log("Checking if group %s is authorized for function '%s' with context '%s' " % (str(groups), functionname, str(context)), 3)

        if not isinstance(groups, list):
            groups = [ groups ]

        cachedResult = self._getCachedIsAuhtorised(groups, functionname, context)
        if cachedResult is not None:
            #return cached result
            return cachedResult

        def doSearch(groupguid, functionname, context):
            searchfilter = self.osis.getFilterObject()
            searchfilter.add('authoriserule', "groupguids", ";" + groupguid + ";", False)
            searchfilter.add('authoriserule', "function", functionname, True)
            rules = self.osis.objectsFindAsView("ui", "authoriserule", searchfilter, 'authoriserule')
            # No rules found
            if not rules:
                q.logger.log("No rules found for group %s" % (str(groups)), 3)
                return False

            for rule in rules:
                ruleContext = json.loads(rule['context'])
                # Remove the '_rulegroup' and '_forceinheritance' items from the saved context.
                # This is only used to map stored rules to rulegroups in the UI
                # And yes, I know it's dirty
                if authorization:
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

        result = False
        for groupguid in groups:
            if not groupguid:
                continue

            if doSearch(groupguid, functionname, context):
                result = True
                break

        #store result in cache
        self._setCachedIsAuthorized(groups, functionname, context, result)
        return result
