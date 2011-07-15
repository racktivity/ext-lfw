__author__ = 'Incubaid'
__tags__ = 'authenticate'
__priority__ = 3

import oauth2 as oauth
import urllib2
import ast
import time
from datetime import datetime, timedelta

class HelperServer(oauth.Server):

    def __init__(self, q):
        oauth.Server.__init__(self)
        self.authenticated = {}
        self.signature_methods = {}
        self.add_signature_method(oauth.SignatureMethod_HMAC_SHA1())
        self.cluster_name = q.config.getConfig('dist_auth')['arakoon']['cluster_name']
        self.q = q
        self.access_token = None
        self.consumer = None

    def getTokenAttributesFromStore(self, tokenKey):
        client = self.q.clients.arakoon.getClient(self.cluster_name)
        if not client.exists(key=tokenKey):
            return False
        return client.get(tokenKey)

    def check_access_token(self, oauth_request):
        try:
            self.q.logger.log('CALLING check_access_token', 2)
            self.verify_request(oauth_request, self.consumer, self.access_token)
            return True
        except oauth.Error, err:
            self.q.logger.log('EXCEPTION inside check_access_token', 2)
            self.q.logger.log(err, 2)
            return False
        return

    def renewToken(self, tokenKey, token):
        client = self.q.clients.arakoon.getClient(self.cluster_name)
        validuntil = (datetime.now() +timedelta(hours=float(self.q.config.getConfig('dist_auth')['main']['lifespan'])))
        validuntil = validuntil.strftime("%s")
        client.set(key=tokenKey, value=str({'validuntil': validuntil, 'tokensecret': token['tokensecret'], \
            'groupguids': token['groupguids'] }))

def _getHeaders(request, q):
    headers = dict()
    for header in request._request.requestHeaders.getAllRawHeaders():
        headers[header[0]] = header[1][0]
    q.logger.log("HEADERS "+ str(headers), 4)
    return headers

def _getAuthHeaders(headers, q):
    authHeader = headers["Authorization"]
    oAuthHeaders = dict()
    for item in authHeader.split(','):
        key, value = item.split('=', 1)
        key = key.strip()
        value = value.strip('"')
        oAuthHeaders[key] = urllib2.unquote(value)
    q.logger.log("OAUTH HEADERS "+ str(oAuthHeaders), 4)
    return oAuthHeaders

def main(q, i, params, tags):
    request = params["request"]
    headers = _getHeaders(request, q)
    if headers.has_key('Authorization') and headers['Authorization'].find('OAuth realm="alkira"') >= 0 :
        helperServer = HelperServer(q)
        oAuthHeaders = _getAuthHeaders(headers, q)
        tokenkey = oAuthHeaders['oauth_token']
        token_attributes = helperServer.getTokenAttributesFromStore(tokenkey)
        if token_attributes:
            token_attributes = ast.literal_eval(token_attributes)
        if not token_attributes:
            q.logger.log("The token key does not exist in the Arakoon store", 4)
            return False
        q.logger.log("token_attributes: "+ str(token_attributes), 4)
        tokensecret = token_attributes['tokensecret']

        #check validuntil
        validuntil = float(token_attributes['validuntil'])
        now = time.time()
        if now > validuntil:
            q.logger.log("The token existing in the Arakoon store is expired", 4)
            return False

        #check if we need to renew
        renewaltime = validuntil - \
            timedelta(hours=float(q.config.getConfig('dist_auth')['main']['lifespan']) * 0.75).seconds
        if now > renewaltime:
            q.logger.log("Renewing the token in the Arakoon store", 4)
            helperServer.renewToken(tokenkey, token_attributes)

        helperServer.consumer = oauth.Consumer(oAuthHeaders['oauth_consumer_key'], '')
        helperServer.access_token = oauth.Token(tokenkey, tokensecret)
        ## <dirty hack> because of reverse proxy in client
        path = request._request.uri

        # Take the substring of path, starting from the first '/' (ignoring the first character)
        index = path.find("/", 1)
        if index > 0:
            path = path[index:]
        http_url = "http://alkira%s" % (path)
        ## </dirty hack>
        parameters = request._request.args
        q.logger.log(params)

        oauth_request = oauth.Request.from_request(request._request.method, http_url, headers=headers,
            parameters=parameters)
        params["result"] = helperServer.check_access_token(oauth_request)
    else:
        #An unauthenticated user cannot access the administration space
        if request._request.uri.find("/appserver/rest/ui/portal/getPage?space=Admin") > 0:
            params["result"] = False
        else:
            params["result"] = True

    #set the http response to 403 when we failed
    if params["result"] == False:
        request._request.setResponseCode(403)
