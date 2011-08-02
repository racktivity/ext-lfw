from alkira import Alkira

def main(q, i, p, params, tags):
    q.logger.log('Creating user %s' % params['name'], 1)
    alkira = Alkira(p.api)
    user = alkira.createUser(login=params['login'], password=params['password'], name=params['name'])
    params['result'] = user.guid

def match(q, i, p, params, tags):
    return True
