from alkira import Alkira

def main(q, i, p, params, tags):
    alkira = Alkira(p.api)
    alkira.revokeRule(params['groupguids'], params['function'], params['context'])
    params['result'] = True

def match(q, i, p, params, tags):
    return True
