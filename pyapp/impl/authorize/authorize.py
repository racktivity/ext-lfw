__author__ = 'Incubaid'
__tags__ = 'authorize'
__priority__ = 3

import copy
from osis.store.OsisDB import OsisDB
from alkira.authservice import AuthService

# For now we depend on racktivity library but support not having it as well
try:
    from racktivity.authorization import RacktivityAuthorizationCrossChecker
except ImportError:
    RacktivityAuthorizationCrossChecker = None

def getConfig(q, p):
    if not getConfig.config:
        getConfig.config = q.tools.inifile.open(q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname, "cfg", \
            "auth.cfg")).getFileAsDict()
    return getConfig.config
getConfig.config = None

def isLocalRequest(request):
    clientIp = None
    for header in request._request.requestHeaders.getAllRawHeaders(): #pylint: disable=W0212
        if header[0] == "X-Forwarded-For":
            clientIp = header[1][0]

    if not clientIp:
        clientIp = request._request.getClientIP() #pylint: disable=W0212
    return clientIp == "localhost" or clientIp == "127.0.0.1"

def isAdminOrIdeSpace(params):
    authInfo = params["criteria"]
    kwargs = params["kwargs"]
    if "authorizeRule" in authInfo and authInfo["authorizeRule"] == "view page" and \
        "space" in kwargs and (kwargs["space"] == "Admin" or kwargs["space"] == "IDE"):

        return True
    return False

def getAllArguments(params):
    arguments = copy.copy(params["kwargs"])

    #add default args
    method = getattr(params["service"], params["methodname"])
    if hasattr(method, "argspec"):
        args, _, _, defaultArgs = method.argspec

        if defaultArgs:
            for i in xrange(0, len(defaultArgs)):
                argName = args[-i - 1]
                if not argName in arguments:
                    arguments[argName] = defaultArgs[i]

    return arguments

def getParamValue(arguments, paramName):
    if paramName in arguments:
        arg = arguments[paramName]
        return arg if arg is not None else ""
    elif not paramName:
        return ""
    elif paramName[0] == '@':
        return paramName[1:]
    else:
        return None

authService = None

def main(q, i, p, params, tags): #pylint: disable=W0613
    global authService #pylint: disable=W0603
    if authService is None:
        authService = AuthService()

    request = params["request"]
    if not request.username:
        params["result"] = False
    else:
        q.logger.log("Checking authorization for user %s with params %s" % (request.username, str(params)), 3)

        config = getConfig(q, p)
        if request.username == "anonymous" and isAdminOrIdeSpace(params):
            #An unauthenticated user cannot access the ADMIN or IDE space
            q.logger.log("An unauthenticated user cannot access the ADMIN or IDE space", 3)
            params["result"] = False
        elif request.username == "anonymous" and isLocalRequest(request) and int(config["auth"]["insecure"]):
            q.logger.log("Allowing authorization for local request", 3)
            params["result"] = True
        else:
            #default unauthorized
            params["result"] = False

            conn = OsisDB().getConnection(p.api.appname)
            searchfilter = conn.getFilterObject()
            searchfilter.add("user", "login", request.username, True)
            users = conn.objectsFindAsView("ui", "user", searchfilter, "user")

            if users and len(users) == 1:
                user = users[0]
                groups = filter(None, user["groupguids"].split(";")) #pylint: disable=W0141

                # we only parse the name in kwargs and the default values
                arguments = getAllArguments(params)
                context = {}
                authInfo = params["criteria"]
                if "authorizeParams" in authInfo:
                    for key, value in authInfo["authorizeParams"].iteritems():
                        if isinstance(value, list):
                            contextValues = list()
                            for val in value:
                                contextValue = getParamValue(arguments, val)
                                if contextValue is not None:
                                    contextValues.append(contextValue)
                            if contextValues:
                                context[key] = contextValues
                            else:
                                # param not found, bailing out
                                params["result"] = False
                                request._request.setResponseCode(412) #pylint: disable=W0212
                                return
                        else:
                            contextValue = getParamValue(arguments, value)
                            if contextValue is not None:
                                context[key] = contextValue
                            else:
                                # param not found, bailing out
                                params["result"] = False
                                request._request.setResponseCode(412) #pylint: disable=W0212
                                return

                funcName = None
                if "authorizeRule" in authInfo:
                    funcName = authInfo["authorizeRule"]

                if funcName:
                    params["result"] = authService.isAuthorised(groups, funcName, context)

                    if not params["result"] and RacktivityAuthorizationCrossChecker is not None:
                        ## Check if we can crosscheck with another wizard
                        authCrossChecker = RacktivityAuthorizationCrossChecker()
                        oldWizard = context.get('wizard')
                        if oldWizard and oldWizard in authCrossChecker.AUTHORIZATION_CROSSCHECK_MAP:
                            newWizard, crosscheckFunction = authCrossChecker.AUTHORIZATION_CROSSCHECK_MAP[oldWizard]
                            newContext = crosscheckFunction(newWizard, context)
                            if newContext:
                                q.logger.log("Rechecking authorization for user %s with new context %s" % (request.username, str(newContext)), 3)
                                params["result"] = authService.isAuthorised(groups, funcName, newContext)

    #set the http response to 405 when we failed
    if params["result"] == False:
        request._request.setResponseCode(405) #pylint: disable=W0212
