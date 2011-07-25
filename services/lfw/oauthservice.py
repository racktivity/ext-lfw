import uuid, os, oauth2
from pylabs import q, p
from datetime import datetime, timedelta

class OAuthService(object):
    def __init__(self):
        self.arakoon_client = q.clients.arakoon.getClient(p.api.appname)
        self.config = q.tools.inifile.open(q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname, "cfg", "oauth.cfg"))

    @q.manage.applicationserver.expose
    def getToken(self, user, password):
        """
        Authenticate the user through a call to an external service
        @param user: user name
        @type user: string

        @param password: password
        @type password: string

        @return: True for a valid user/password combination, and False otherwise and a list of group IDs for the user
        @rtype: list
        """

        valid, groupguids = False, ()

        #special handling for the admin user
        if user.lower() == 'admin':
            valid = self._checkAdminCredentials(user, password)

        #if not valid:
            #servicename = self.config['main']['servicename']
            #backend_service_mod = self._loadBackEndService(servicename)
            #backend_service = backend_service_mod(self.config[servicename], user, password)

            ##Authenticate the user using the Auth service
            #valid, groupguids = backend_service.isAuthenticated(user, password), ()

        if not valid:
            q.logger.log('Invalid user name/password combination', 4)
            raise Warning("Invalid user name/password combination")

        q.logger.log('Request sent for authentication, user: %s' % user, 3)
        try:
            token = oauth2.Token(str(uuid.uuid4()), str(uuid.uuid4()))
            token.set_verifier('')

            self.saveToArakoon(token, groupguids=groupguids)

            q.logger.log('OAuth token generated, and saved to Arakoon cluster', 3)
            return token.to_string()
        except oauth2.Error, err:
            q.logger.log('Exception while generating token %s' % str(err), 4)
            raise Warning('Exception while generating token %s' % str(err))

    def saveToArakoon(self, token, groupguids=None):
        """
        Save  the generated OAuth token to the pyapps Arakoon cluster in the form: key='token_$(token_key)', value='token_secret'
        @param token: tokenkey, and tokensecret
        @type user name: string

        @return:
        @rtype:

        @raise :
        """
        parts = str(token).split('&')
        tokenkey = None
        tokensecret = None
        if parts[0].startswith("oauth_token_secret"):
            tokensecret = parts[0].split('=')[1]
            tokenkey = parts[1].split('=')[1]
        else:
            tokenkey = parts[0].split('=')[1]
            tokensecret = parts[1].split('=')[1]
        validhours = self.config.getFloatValue("oauth", "hoursvalid")
        validuntil = (datetime.now() + timedelta(hours=validhours)).strftime("%s")
        q.logger.log("Saving to Arakoon tokenkey: token_$(%s), tokensecret:%s" % (tokenkey, tokensecret), 3)
        self.arakoon_client.set(key='token_$(%s)' % tokenkey, value=str({'validuntil': validuntil, \
            'tokensecret':tokensecret, 'groupguids':groupguids}))

    def _loadBackEndService(self, servicename):
        plugin = None
        pluginsdir = os.path.dirname(__file__)
        if not pluginsdir:
            pluginsdir = "."
        candidates = os.listdir(pluginsdir)
        for candidate in candidates:
            if candidate == "__init__.py" or not candidate.endswith(".py"):
                continue
            modname = os.path.splitext(candidate)[0]
            if modname != servicename:
                continue
            pluginmod = __import__(modname, level=1)
            if hasattr(pluginmod, 'BACKEND'):
                plugin = getattr(pluginmod, 'BACKEND')
        return plugin

    def _checkAdminCredentials(self, adminuser, adminpassword):
        if adminuser == "admin" and adminpassword == "admin":
            return True
        return False
