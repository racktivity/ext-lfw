def main(q, i, p, params, tags):
    q.logger.log('Creating config %s/%s/%s/%s' % (params['space'], params['name'], params['macro'], params['configid'] if params['configid'] else ""), 1)
    alkira = q.clients.alkira.getClientByApi(p.api)
    alkira.updateMacroConfig(space=params['space'],
                      page=params['page'],
                      macro=params['macro'],
                      config=params['config'],
                      configid=params['configid'] if params['configid'] else None)

    params['result'] = True

def match(q, i, p, params, tags):
    return True
