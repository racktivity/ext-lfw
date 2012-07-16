__tags__ = 'schedule'
__author__ = 'incubaid'

import ast, time
from alkira import oauthservice

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    table = osis.findTable(oauthservice.TABLE_SCHEMA, oauthservice.TABLE_NAME)

    deleteList = []
    try:
        tokens = osis.runSqlAlchemyQuery(table.select())
        for token in tokens:
            data = dict(token)
            parsedVal = ast.literal_eval(data["value"])
            currentTime = time.time()
            if currentTime > float(parsedVal['validuntil']):
                deleteList.append(data["key"])
    except Exception as e:
        q.logger.log("Got exception while cleaning up OAuth tokens: %s" % str(e), 4)

    for delkey in deleteList:
        q.logger.log("Deleting expired token from Arakoon cluster, token_key: %s" % delkey, 3)
        osis.runSqlAlchemyQuery(table.delete().where(table.c.key == delkey))

def match(q, i, p, params, tags):
    config = q.tools.inifile.open(q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname, "cfg", "auth.cfg"))
    if config.checkParam("oauth", "tokencleanup"):
        return (params['taskletlastexecutiontime']  + (60 * config.getIntValue("oauth", "tokencleanup")) <= time.time())
    else:
        return False
