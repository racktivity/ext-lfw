def main(q, i, p, params, tags):

    alkira = q.clients.alkira.getClientByApi(p.api)

    alkira.updateMacroConfig(space=params['space'],
                      page=params['page'],
                      macro=params['macro'],
                      config=params['config'],
                      username=params['username'],
                      configid=params['configid'] if params['configid'] else None)

    params['result'] = True

def match(q, i, p, params, tags):
    return True
