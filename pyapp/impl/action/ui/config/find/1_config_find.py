def main(q, i, p, params, tags):
    alkira = q.clients.alkira.getClientByApi(p.api)
    result = alkira.findMacroConfig(space=params['space'],
                    page=params['page'],
                    macro=params['macro'],
                    configid=params['configid'],
                    exact_properties=params['exact_properties'])

    params['result'] = result
