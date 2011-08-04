from alkira import Alkira

def main(q, i, p, params, tags):
    q.logger.log('Creating rule for %s with function %s and context %s' % \
        (params['groupguids'], params['function'], params['context']), 1)
    alkira = Alkira(p.api)
    alkira.assignRule(params['groupguids'], params['function'], params['context'])

    params['result'] = True

def match(q, i, p, params, tags):
    return True
