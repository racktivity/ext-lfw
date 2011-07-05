def main(q, i, p, params, tags):
    q.logger.log('Creating user %s' % params['name'], 1)
    alkira = q.clients.alkira.getClientByApi(p.api)
    user = alkira.createUser(name=params['name'],
                             password=params['password'],
                             spaces=params['spaces'],
                             pages=params['pages'],
                             tagsList=params.get('tags', '').split(" "))
    params['result'] = user.guid

def match(q, i, p, params, tags):
    return True
