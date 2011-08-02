__author__ = 'Incubaid'
__tags__ = 'authorize', 'authbackend'
__priority__ = 3

import xmlrpclib, httplib
from osis.store.OsisDB import OsisDB

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

def main(q, i, p, params, tags):
    request = params["request"]

    if not request.username:
        config = q.tools.inifile.open(q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname, "cfg", \
            "auth.cfg")).getFileAsDict()
        if int(config["auth"]["insecure"]):
            params["result"] = True
        else:
            params["result"] = False
    else:
        q.logger.log("Checking authorization for user %s" % request.username, 3)

        #default unauthorized
        params["result"] = False

        conn = OsisDB().getConnection(p.api.appname)
        searchfilter = conn.getFilterObject()
        searchfilter.add("ui_view_user_list", "login", request.username, True)
        users = conn.objectsFindAsView("ui", "user", searchfilter, "ui_view_user_list")

        if users and len(users) == 1:
            user = users[0]
            groups = filter(None, user["groupguids"].split(";"))

            #
            # Normally this part isn't needed because we have the Auth service but because we cannot call the service
            # from inside the authorize tasklet (because this is implemented in the main thread of the appserver).
            # So we just do the same as the Auth service is doing and then use the backend directly.
            # This is why the "authbackend" tag is added
            #

            authBackend = params["authbackend"]

            # we only parse the name in kwargs
            context = {}
            if "space" in params["kwargs"]:
                context["name"] = params["kwargs"]["space"]
            elif "name" in params["kwargs"]:
                context["name"] = params["kwargs"]["name"]
            params["result"] = authBackend.isAuthorised(groups, params["methodname"], context)

    #set the http response to 405 when we failed
    if params["result"] == False:
        request._request.setResponseCode(405)
