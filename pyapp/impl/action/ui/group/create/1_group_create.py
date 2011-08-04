from alkira import Alkira

def main(q, i, p, params, tags):
    q.logger.log('Creating group %s' % params['name'], 1)
    alkira = Alkira(p.api)

    params['result'] = alkira.createGroup(params['name'])

def match(q, i, p, params, tags):
    return True
