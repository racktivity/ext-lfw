from alkira import Alkira

def main(q, i, p, params, tags):
    alkira = Alkira(p.api)
    result = alkira.findMacroConfig(space=params['space'],
                    page=params['page'],
                    macro=params['macro'],
                    configid=params['configid'],
                    username=params['username'],
                    exact_properties=params['exact_properties'])

    params['result'] = result
