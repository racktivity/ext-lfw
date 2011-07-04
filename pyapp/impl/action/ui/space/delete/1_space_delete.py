def main(q, i, p, params, tags):
    alkira = q.clients.alkira.getClientByApi(p.api)
    alkira.deleteSpace(params['spaceguid'])
    params['result'] = True
    
def match(q, i, p, params, tags):
    return True
