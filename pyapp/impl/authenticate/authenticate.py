__author__ = 'Incubaid'
__tags__ = 'authenticate'
__priority__ = 3

import oauth2 as oauth
import urllib2
import ast
import time
from datetime import datetime, timedelta
from alkira import oauthservice

class HelperServer(oauth.Server):
    def __init__(self, q, p, config):
        oauth.Server.__init__(self)
        self.authenticated = {}
        self.signature_methods = {}
        self.add_signature_method(oauth.SignatureMethod_HMAC_SHA1())
        self.q = q
        self.p = p
        self.access_token = None
        self.consumer = None
        self.config = config
        self.osis = self.p.application.getOsisConnection(self.p.api.appname)
        self.table = self.osis.findTable(oauthservice.TABLE_SCHEMA, oauthservice.TABLE_NAME)

    def getTokenAttributesFromStore(self, tokenKey):
        select = self.table.select().where(self.table.c.key == tokenKey)
        data = self.osis.runSqlAlchemyQuery(select).fetchone()
        if not data:
            return False
        tokenAttributes = dict(data)["value"]
        if not tokenAttributes:
            return False
        return tokenAttributes

    def checkAccessToken(self, oauthRequest, url):
        try:
            self.verify_request(oauthRequest, self.consumer, self.access_token)
            return True
        except oauth.Error, err:
            self.q.logger.log('EXCEPTION inside check_access_token for %s' % url, 4)
            self.q.logger.log(err, 4)
            return False
        return

    def renewToken(self, tokenKey, token):
        validhours = float(self.config["oauth"]["hoursvalid"])
        validuntil = (datetime.now() +timedelta(hours=validhours)).strftime("%s")

        value = str({'validuntil': validuntil, 'tokensecret': token['tokensecret'] })
        update = self.table.update().where(self.table.c.key == tokenKey).values(value=value)
        self.osis.runSqlAlchemyQuery(update)

def _getHeaders(request, q):
    headers = dict()
    for header in request._request.requestHeaders.getAllRawHeaders():
        headers[header[0]] = header[1][0]
    q.logger.log("HEADERS "+ str(headers), 5)
    return headers

def _getAuthHeaders(headers, q):
    authHeader = headers["Authorization"]
    oAuthHeaders = dict()
    for item in authHeader.split(','):
        key, value = item.split('=', 1)
        key = key.strip()
        value = value.strip('"')
        oAuthHeaders[key] = urllib2.unquote(value)
    q.logger.log("OAUTH HEADERS "+ str(oAuthHeaders), 5)
    return oAuthHeaders

def getConfig(q, p):
    if not getConfig.config:
        getConfig.config = q.tools.inifile.open(q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname, "cfg", \
            "auth.cfg")).getFileAsDict()
    return getConfig.config
getConfig.config = None

def main(q, i, p, params, tags):
    request = params["request"]
    headers = _getHeaders(request, q)
    if headers.has_key('Authorization') and headers['Authorization'].find('OAuth realm="alkira"') >= 0:
        config = config = getConfig(q, p)
        helperServer = HelperServer(q, p, config)
        oAuthHeaders = _getAuthHeaders(headers, q)
        tokenkey = oAuthHeaders['oauth_token']
        tokenAttributes = helperServer.getTokenAttributesFromStore(tokenkey)
        if tokenAttributes:
            tokenAttributes = ast.literal_eval(tokenAttributes)
        if not tokenAttributes:
            q.logger.log("The token key does not exist in the OSIS store", 4)
            params["result"] = False
        else:
            q.logger.log("token_attributes: " + str(tokenAttributes), 5)
            tokensecret = tokenAttributes['tokensecret']

            #check validuntil
            validuntil = float(tokenAttributes['validuntil'])
            now = time.time()
            if now > validuntil:
                q.logger.log("The token existing in the OSIS store is expired", 4)
                params["result"] = False
            else:
                #check if we need to renew
                validhours = float(config["oauth"]["hoursvalid"])
                renewaltime = validuntil - \
                    timedelta(hours=validhours * 0.75).seconds
                if now > renewaltime:
                    q.logger.log("Renewing the token in the OSIS store", 3)
                    helperServer.renewToken(tokenkey, tokenAttributes)

                helperServer.consumer = oauth.Consumer(oAuthHeaders['oauth_consumer_key'], '')
                helperServer.access_token = oauth.Token(tokenkey, tokensecret)
                ## <dirty hack> because of reverse proxy in client
                path = request._request.uri

                # Take the substring of path, starting from the first '/' (ignoring the first character)
                index = path.find("/", 1)
                if index > 0:
                    path = path[index:]
                httpUrl = "http://alkira%s" % (path)
                ## </dirty hack>
                parameters = request._request.args

                oauthRequest = oauth.Request.from_request(request._request.method, httpUrl, headers=headers,
                    parameters=parameters)
                params["result"] = helperServer.checkAccessToken(oauthRequest, httpUrl)

                #set the username so this can be used in the authorize tasklet
                request.username = oAuthHeaders['oauth_consumer_key']
    else:
        request.username = "anonymous"
        params["result"] = True

    #set the http response to 403 when we failed
    if params["result"] == False:
        request._request.setResponseCode(403)
