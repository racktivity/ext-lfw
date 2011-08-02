from pylabs import q, p

import urllib
import httplib
import json

class AlkiraClient:

    def getClient(self, hostname, appname, port=80):
        """
        Gets a client object.

        @type hostname: String
        @param hostname: The IP that the Alkira Client will use to get a connection and add the pages.

        @return: A client object.
        """
        return Client(hostname, appname, port=port)

class Client:
    def __init__(self, hostname, appname, port=80):
        """
        Initialize a new Alkira Client with the given (hostname, appname) connection
        but if hostname and appname are not given, the given api is used

        @param hostname: The hostname of alikra
        @param appname: The application name
        @param port: Alkira Web port
        """

        self.__hostname = hostname
        self.__port = port
        self.__appname = appname

    @property
    def hostname(self):
        return self.__hostname

    @property
    def appname(self):
        return self.__appname

    @property
    def port(self):
        return self.__port

    def __call(self, method, **args):
        data = {}
        #only pass arguments that has value
        for k, v in args.iteritems():
            if v != None:
                data[k] = json.dumps(v)

        data = urllib.urlencode(data)
        headers = {'Content-Type': "application/x-www-form-urlencoded"}

        con = httplib.HTTPConnection(self.hostname, self.port)
        try:
            con.request("POST",'/%(appname)s/appserver/rest/ui/portal/%(method)s' % {'appname': self.appname,
                                                                                            'method': method}, body=data, headers=headers)
            res = con.getresponse()
            body = json.loads(res.read())
            if res.status == 200:
                return body
            else:
                raise Exception(body['exception'] if 'exception' in body else res.reason, res.status)
        finally:
            con.close()

    def tags(self, space=None, term=None):
        return self.__call('tags', space=space, term=term)

    def listSpaces(self, term=None):
        return self.__call('listSpaces', term=term)

    def createSpace(self, name, tags="", order=None):
        return self.__call("createSpace", name=name, tags=tags, order=order)

    def updateSpace(self, name, newname=None, tags=""):
        return self.__call("updateSpace", name=name, newname=newname, tags=tags)

    def deleteSpace(self, name):
        return self.__call("deleteSpace", name=name)

    def listUsers(self, login=None):
        return self.__call("listUsers", login=login)

    def getUserInfo(self, login):
        return self.__call("getUserInfo", login=login)

    def createUser(self, login, name=None, password=None):
        return self.__call("createUser", login=login, password=password, name=name)

    def deleteUser(self, userguid):
        return self.__call("deleteUser", userguid=userguid)

    def updateUser(self, userguid, name=None, password=None):
        return self.__call("updateUser", userguid=userguid, name=name, password=password)

    def addUserToGroup(self, userguid, groupguid):
        return self.__call("addUserToGroup", userguid=userguid, groupguid=groupguid)

    def removeUserFromGroup(self, userguid, groupguid):
        return self.__call("removeUserFromGroup", userguid=userguid, groupguid=groupguid)

    def createGroup(self, name):
        return self.__call("createGroup", name=name)

    def deleteGroup(self, groupguid):
        return self.__call("deleteGroup", groupguid=groupguid)

    def listGroups(self, name=None):
        return self.__call("listGroups", name=name)

    def getGroupInfo(self, name):
        return self.__call("getGroupInfo", name=name)

    def updateGroup(self, groupguid, name):
        return self.__call("updateGroup", groupguid=groupguid, name=name)

    def assignRule(self, groupguids, function, context):
        return self.__call("assignRule", groupguids=groupguids, function=function, context=context)

    def revokeRule(self, groupguids, function, context):
        return self.__call("revokeRule", groupguids=groupguids, function=function, context=context)

    def listPages(self, space=None, term=None):
        return self.__call("listPages", space=space, term=term)

    def countPages(self, space=None):
        return self.__call("countPages", space=space)

    def categories(self, space=None, term=None):
        return self.__call("categories", space=space, term=term)

    def search(self, text=None, space=None, category=None, tags=None):
        return self.__call("search", text=text, space=space, category=category, tags=tags)

    def breadcrumbs(self, space, name):
        return self.__call("breadcrumbs", space=space, name=name)

    def getSpace(self, space):
        return self.__call("getSpace", space=space)

    def getPage(self, space, name):
        return self.__call("getPage", space=space, name=name)

    def createPage(self, space, name, content, parent=None, order=None, title=None, tags="", category='portal', pagetype="md"):
        return self.__call("createPage", space=space, name=name, content=content,
                           parent=parent, order=order, title=title, tags=tags, category=category, pagetype=pagetype)

    def updatePage(self, space, name, content, newname=None, parent=None, order=None, title=None, tags="", category=None, pagetype=None):
        return self.__call("updatePage", space=space, name=name, content=content,
                           newname=newname, parent=parent, order=order, title=title,
                           tags=tags, category=category, pagetype=pagetype)

    def deletePage(self, space, name):
        return self.__call("deletePage", space=space, name=name)

    def importSpace(self, space, filename, cleanImport=True):
        return self.__call("importSpace", space=space, filename=filename, cleanImport=cleanImport)

    def exportSpace(self, space, filename):
        return self.__call("exportSpace", space=space, filename=filename)

    def hgPushSpace(self, space, repository, repo_username, repo_password=None):
        return self.__call("hgPushSpace", space=space, repository=repository,
                           repo_username=repo_username, repo_password=repo_password)

    def hgPullSpace(self, space, repository, repo_username, repo_password=None, dontSync=False):
        return self.__call("hgPullSpace", space=space, repository=repository,
                           repo_username=repo_username, repo_password=repo_password, dontSync=dontSync)

    def macroConfig(self, space, page, macro, configId=None):
        return self.__call("macroConfig", space=space, page=page, macro=macro, configId=configId)

    def updateMacroConfig(self, space, page, macro, config, configId=None):
        return self.__call("updateMacroConfig", space=space, page=page, macro=macro, config=config, configId=configId)

