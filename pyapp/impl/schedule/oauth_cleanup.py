__tags__ = 'schedule'
__author__ = 'incubaid'

import ast, time

def main(q, i, p, params, tags):
    arakoon_client = q.clients.arakoon.getPoolClient(p.api.appname)
    deleteList = []
    try:
        tokens = arakoon_client.range(beginKey="token_$(", beginKeyIncluded=True, endKey="tokeo", endKeyIncluded=False)
        for token in tokens:
            if not token.startswith('token_$('):
                #this key is not related to the Authentication service
                continue
            value = arakoon_client.get(token)
            parsedVal = ast.literal_eval(value)
            currentTime = time.time()
            if currentTime > float(parsedVal['validuntil']):
                deleteList.append(token)
    except Exception as e:
        q.logger.log("Got exception while cleaning up OAuth tokens: %s" % str(e), 4)
    for delkey in deleteList:
        if arakoon_client.exists(delkey):
            q.logger.log("Deleting expired token from Arakoon cluster, token_key: %s" % delkey, 3)
            arakoon_client.delete(delkey)

def match(q, i, p, params, tags):
    config = q.tools.inifile.open(q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname, "cfg", "auth.cfg"))
    if config.checkParam("oauth", "tokencleanup"):
        return (params['taskletlastexecutiontime']  + (60 * config.getIntValue("oauth", "tokencleanup")) <= time.time())
    else:
        return False
