
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import urllib
import oauth2 as oauth
import ConfigParser
import urlparse
import os
import SocketServer
import socket
import threading
import time
from datetime import datetime, timedelta
import uuid
from pylabs.InitBaseCore import q
import json
import httplib
import ast
import optparse


class RequestHandler(BaseHTTPRequestHandler):
    def authenticateUser(self, username, password):
        """
        Authenticate the user through a call to the ECS service
        @param username: user name
        @type user name: string

        @param password: password
        @type password: string
        
        @return: True for a valid user/password combination, and False otherwise and a list of group IDs for the user
        @rtype: list
        """
        return True, ()

    def call(self, method="useraccess", **args):
        """
        Make an HTTP post request to the ECS service
        @param method: name of the method exposed by the ECS service, default is 'useraccess'
        @type user name: string

        @param args: example: login='test', password='123'
        @type args: list of key/value pairs
        
        @return: list of user access permissions
        @rtype: list
        """
        con = httplib.HTTPConnection(self.server.config['ecs']['ip'], self.server.config['ecs']['port'])
        data = json.dumps(args)
        headers = {'Content-Type': "application/vap.racktivity.com.%s+json" % (method),
                   'Content-Length': len(data)}
        con.request("POST", "/%s" % method, body=data, headers=headers)
        res = con.getresponse()
        if res.status == 200:
            return json.loads(res.read())
        else:
            q.logger.log("Exception while calling the ECS service: %s %s"%(str(res.status), str(res.reason)) )
            return [0,]

    def saveToArakoon(self, token, longlast=False, groupguids=None):
        """
        Save  the generated OAuth token to the racktivity Arakoon cluster in the form: key='token_$(token_key)', value='token_secret'
        @param token: tokenkey, and tokensecret
        @type user name: string

        @return: 
        @rtype: 

        @raise : 
        """
        parts = str(token).split('&')
        tokenkey = None; tokensecret = None
        if parts[0].startswith("oauth_token_secret"):
            tokensecret = parts[0].split('=')[1]
            tokenkey = parts[1].split('=')[1]
        else:
            tokenkey = parts[0].split('=')[1]
            tokensecret = parts[1].split('=')[1]
        if longlast:
            validuntil = (datetime.now() +timedelta(hours=24)).strftime("%s")
        else:
            validuntil = (datetime.now() +timedelta(hours=float(self.server.config['main']['lifespan']))).strftime("%s")
        q.logger.log("Saving to Arakoon tokenkey: token_$(%s), tokensecret:%s"%(tokenkey,tokensecret), 2)
        self.server.arakoon_client.set(key='token_$(%s)'%tokenkey, value=str({'validuntil': validuntil, \
                                                          'tokensecret':tokensecret, 'groupguids':groupguids}))

    def do_GET(self):
        """
        Handles the GET/POST request to generate an OAuth access token
        """
        data = dict()
        #reading posted data
        postdata = None
        if self.command == "POST":
            try: 
                length = int(self.headers.getheader('content-length'))
                postdata = self.rfile.read(length)
                data.update(self.parseQuery(postdata))
            except:
                pass
        else:
            path = urlparse.urlparse(self.path)
            data.update(self.parseQuery(path.query))
        jsonp = None
        
        if not (data.has_key('user') and data.has_key('password')):
            q.logger.log('user name and/or password not found in the request', 2)
            #self.send_response(401)
            self.wfile.write("401: user name and/or password not found in the request")
            self.wfile.close()
            return
        jsonp = data.pop("_jsonp", None)
        #Authenticate the user using the ECS
        valid, groupguids = self.authenticateUser(data['user'], data['password'])
        if not valid:
            q.logger.log('Invalid user name/password combination', 2)
            #self.send_response(401)
            self.wfile.write("401: Invalid user name/password combination")
            self.wfile.close()
            return

        if self.path.startswith(self.server.config['main']['access_path']):
            q.logger.log('Request sent for authentication, user:%s'%data['user'], 2)
            try:
                #Generate a new access token
                oauth_request = oauth.Request.from_request(self.command, '%s%s' % (self.server.config['main']['host'], self.path), headers=self.headers)
                token = oauth.Token(str(uuid.uuid1()), str(uuid.uuid1()))
                token.set_verifier('')
                self.send_response(200)
                if jsonp:
                    self.send_header("Content-Type", "application/javascript")
                else:
                    self.send_header("Content-type", "text/html")
                self.end_headers()
                if data.has_key('longlast'):
                    self.saveToArakoon(token, longlast=True, groupguids=groupguids)
                else:
                    self.saveToArakoon(token, groupguids=groupguids)
                q.logger.log('OAuth token generated, and saved to Arakoon cluster', 2)
                if jsonp:
                    self.wfile.write("%s(%s);" % (jsonp, json.dumps(token.to_string())))
                else:
                    self.wfile.write(token.to_string())
                self.wfile.close()
            except oauth.Error, err:
                q.logger.log('Exception while generating token %s'%str(err), 2)
                self.send_oauth.error(err)

    def do_POST(self):
        return self.do_GET()


    def parseQuery(self, query):
        paramsparts = query.split("&")
        params = {}
        for paramstr in paramsparts:
            if not paramstr:
                continue
            pp = paramstr.split("=")
            params[urllib.unquote(pp[0])] = urllib.unquote(pp[1])
        
        return params


class TokensCleanup(threading.Thread):
    def run(self):
        key = None
        deleteList=[]
        while self.loop:
            try:
                keys = self.arakoon_client.range(beginKey='a', beginKeyIncluded=True, endKey='z', endKeyIncluded=True)
                for key in keys:
                    if not key.startswith('token_$('):
                        #this key is not related to the Authentication service
                        continue
                    value = self.arakoon_client.get(key)
                    parsedVal = ast.literal_eval(value)
                    currentTime = time.time()
                    if  currentTime > float(parsedVal['validuntil']):
                        deleteList.append(key)
            except Exception:
                deleteList.append(key)
            for delkey in deleteList:
                if self.arakoon_client.exists(delkey):
                    q.logger.log('Deleting expired token from Arakoon cluster, token_key:%s'%delkey, 2)
                    self.arakoon_client.delete(delkey)
            del deleteList[:]

            time.sleep(float(self.timetosleep))


class DistributedAuth(SocketServer.ThreadingTCPServer):
    def __init__(self):
        SocketServer.ThreadingTCPServer.__init__(self, ("0.0.0.0", 6543), RequestHandler, bind_and_activate=False)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_bind()
        self.server_activate()
    def start(self):
        self.serve_forever()


def main():
    config = q.config.getConfig('dist_auth')
    parser = optparse.OptionParser()
    parser.add_option("-p", "--pid", dest="pidfile", help="PID file")
    options, args = parser.parse_args()
    if not options.pidfile:
        parser.error("-p is required option")
    q.system.fs.writeFile(options.pidfile, str(os.getpid()))
    try:
        arakoon_client = q.clients.arakoon.getClient(config['arakoon']['cluster_name'])
        cleanup = TokensCleanup()
        cleanup.loop = True
        cleanup.timetosleep = config["main"]["sleep_period"]
        cleanup.arakoon_client = arakoon_client 
        cleanup.start()
        da = DistributedAuth()
        da.config = config
        da.arakoon_client = arakoon_client
        da.start()

    except KeyboardInterrupt:
        q.logger.log("OAuth Server closing...", 2)
        cleanup.loop = False
    finally:
        q.system.fs.removeFile(options.pidfile)
        os.sys.exit()

if __name__ == '__main__':
    main()