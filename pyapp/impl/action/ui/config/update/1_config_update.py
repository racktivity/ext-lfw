from alkira import Alkira

def main(q, i, p, params, tags):

    alkira = Alkira(p.api)

    alkira.updateMacroConfig(space=params['space'],
                      page=params['page'],
                      macro=params['macro'],
                      config=params['config'],
                      username=params['username'],
                      configid=params['configid'] if params['configid'] else None)

    params['result'] = True

def match(q, i, p, params, tags):
    return True
