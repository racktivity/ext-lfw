def main(q, i, p, params, tags):
    alkira = q.clients.alkira.getClientByApi(p.api)
    alkira.deletePageByGUID(params['pageguid'])
    params['result'] = True
    
def match(q, i, p, params, tags):
    return True
