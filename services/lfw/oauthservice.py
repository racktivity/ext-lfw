import uuid, oauth2, httplib, xmlrpclib, sqlalchemy
from pylabs import q, p
from datetime import datetime, timedelta

TABLE_NAME = "oauth_token"
TABLE_SCHEMA = "ui"

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

class OAuthService(object):
    def __init__(self):
        self.osis = p.application.getOsisConnection(p.api.appname)

        self.token_table = sqlalchemy.Table(self.osis._getTableName(TABLE_SCHEMA, TABLE_NAME),
            self.osis._sqlalchemy_metadata,
            sqlalchemy.Column("key", sqlalchemy.String(60), primary_key=True, nullable=False),
            sqlalchemy.Column("value", sqlalchemy.String(100)),
            schema=self.osis._getSchemeName(TABLE_SCHEMA, TABLE_NAME)
        )

        if not self.token_table.exists(self.osis._sqlalchemy_engine):
            self.token_table.create(self.osis._sqlalchemy_engine)

        config = q.tools.inifile.open(q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname, "cfg", "auth.cfg"))
        self.config = config.getFileAsDict()

        config = q.tools.inifile.open(q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname, "cfg", \
            "applicationserver.cfg"))
        self.xmlrpcUrl = "http://%s:%d/RPC2" % (config.getValue("main", "xmlrpc_ip"), \
            config.getIntValue("main", "xmlrpc_port"))

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

        valid = TimeoutServerProxy(self.xmlrpcUrl).ui.auth.verifyUserIdentity(user, password)

        if not valid:
            q.logger.log('Invalid user name/password combination', 4)
            raise Warning("Invalid user name/password combination")

        q.logger.log('Request sent for authentication, user: %s' % user, 3)
        try:
            token = oauth2.Token(str(uuid.uuid4()), str(uuid.uuid4()))
            token.set_verifier('')

            self.saveToken(token)

            q.logger.log('OAuth token generated, and saved', 3)
            return token.to_string()
        except oauth2.Error, err:
            q.logger.log('Exception while generating token %s' % str(err), 4)
            raise Warning('Exception while generating token %s' % str(err))

    def saveToken(self, token):
        """
        Save the generated OAuth token to OSIS in the form: key='token_$(token_key)', value='token_secret'
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
        validhours = float(self.config["oauth"]["hoursvalid"])
        validuntil = (datetime.now() + timedelta(hours=validhours)).strftime("%s")
        q.logger.log("Saving to OSIS tokenkey: token_$(%s), tokensecret:%s" % (tokenkey, tokensecret), 3)

        value = str({ 'validuntil': validuntil, 'tokensecret': tokensecret })
        insert = self.token_table.insert().values(key='token_$(%s)' % tokenkey, value=value)
        self.osis.runSqlAlchemyQuery(insert)
