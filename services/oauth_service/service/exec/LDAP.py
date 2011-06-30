import ldap
from backend import BackEnd

class LDAPClient(BackEnd):
    def __init__(self, config, user, password):
        self.hostname = config['hostname']
        self.port = int(config['port'])
        self.bind = "cn=%s,%s,%s" % (user, config['people_rdn'], config['base_dn']) 
        self.password = password
        self.connection = ldap.open(self.hostname, self.port)
        try:
            self.connection.simple_bind_s(self.bind, self.password)
        except:
            self.connection = None
        self.base_dn = config["base_dn"]
        self.groups_rdn = config["groups_rdn"]
        self.people_rdn = config["people_rdn"]

    def isAuthenticated(self, login, password):
        dn = "cn=%s,%s,%s" % (login, self.people_rdn, self.base_dn)
        l = ldap.open(self.hostname, self.port)
        try:
            l.simple_bind_s(dn, password)
        except:
            return False
        return True

    def listUserGroups(self, login):
        dn = "%s,%s" % (self.groups_rdn, self.base_dn)
        filter = "cn=%s,%s,%s" % (login, self.people_rdn, self.base_dn)
        groups = self.connection.search_s(dn, ldap.SCOPE_SUBTREE, filterstr='(member=%s)' % filter, attrlist=['cn'])
        groupnames = []
        for groupdb, attrs in groups:
            cn = attrs['cn']
            groupnames.append(cn[0])
        return groupnames

    def listGroups(self):
        dn = ",".join((self.groups_rdn, self.base_dn))
        groups = self.connection.search_s(dn, ldap.SCOPE_SUBTREE, attrlist=['cn'])
        groupnames = []
        for groupdb, attrs in groups:
            if 'cn' in attrs:
                cn = attrs['cn']
                groupnames.append(cn[0])
        return groupnames

BACKEND = LDAPClient
