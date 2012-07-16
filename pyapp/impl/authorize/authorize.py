__author__ = 'Incubaid'
__tags__ = 'authorize'
__priority__ = 3

import copy, xmlrpclib, httplib
from osis.store.OsisDB import OsisDB
from osis.store import OsisConnection

from racktivity.authorization import RacktivityAuthorizationCrossChecker

class TimeoutHTTPConnection(httplib.HTTPConnection):
    def connect(self):
        httplib.HTTPConnection.connect(self)
        self.sock.settimeout(self.timeout)

class TimeoutHTTP(httplib.HTTP):
    _connection_class = TimeoutHTTPConnection
    def set_timeout(self, timeout):
        self._conn.timeout = timeout

class TimeoutTransport(xmlrpclib.Transport):
    def __init__(self, timeout=10, *args, **kwargs):
        xmlrpclib.Transport.__init__(self, *args, **kwargs)
        self.timeout = timeout

    def make_connection(self, host):
        conn = TimeoutHTTP(host)
        conn.set_timeout(self.timeout)
        return conn

class TimeoutServerProxy(xmlrpclib.ServerProxy):
    def __init__(self, uri, timeout=10, *args, **kwargs):
        kwargs['transport'] = TimeoutTransport(timeout=timeout, use_datetime=kwargs.get('use_datetime', 0))
        xmlrpclib.ServerProxy.__init__(self, uri, *args, **kwargs)

def getConfig(q, p):
    if not getConfig.config:
        getConfig.config = q.tools.inifile.open(q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname, "cfg", \
            "auth.cfg")).getFileAsDict()
    return getConfig.config
getConfig.config = None

def getAppserverConfig(q, p):
    if not getAppserverConfig.config:
        getAppserverConfig.config = q.tools.inifile.open(q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname, "cfg", \
            "applicationserver.cfg")).getFileAsDict()
    return getAppserverConfig.config
getAppserverConfig.config = None

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
    args, _, _, defaultArgs = getattr(params["service"], params["methodname"]).argspec

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

def main(q, i, p, params, tags): #pylint: disable=W0613
    request = params["request"]
    userTable = OsisConnection.getTableName(domain = 'ui', objType = 'user')
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
            searchfilter.add(userTable, "login", request.username, True)
            users = conn.objectsFindAsView("ui", "user", searchfilter, userTable)

            if users and len(users) == 1:
                user = users[0]
                groups = filter(None, user["groupguids"].split(";")) #pylint: disable=W0141

                appconfig = getAppserverConfig(q, p)
                appserverUrl = "http://%s:%d/RPC2" % (appconfig["main"]["xmlrpc_ip"], int(appconfig["main"]["xmlrpc_port"]))

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
                    appserver = TimeoutServerProxy(appserverUrl, 2)
                    params["result"] = appserver.ui.auth.isAuthorised(groups, funcName, context)

                    if not params["result"]:
                        ## Check if we can crosscheck with another wizard
                        authCrossChecker = RacktivityAuthorizationCrossChecker()
                        oldWizard = context.get('wizard')
                        if oldWizard and oldWizard in authCrossChecker.AUTHORIZATION_CROSSCHECK_MAP:
                            newWizard, crosscheckFunction = authCrossChecker.AUTHORIZATION_CROSSCHECK_MAP[oldWizard]
                            newContext = crosscheckFunction(newWizard, context)
                            if newContext:
                                q.logger.log("Rechecking authorization for user %s with new context %s" % (request.username, str(newContext)), 3)
                                params["result"] = appserver.ui.auth.isAuthorised(groups, funcName, newContext)

    #set the http response to 405 when we failed
    if params["result"] == False:
        request._request.setResponseCode(405) #pylint: disable=W0212
