def main(q, i, p, params, tags):
    alkira = q.clients.alkira.getClientByApi(p.api)
    alkira.deleteUserByGUID(params['userguid'])
    params['result'] = True
    
def match(q, i, p, params, tags):
    return True
