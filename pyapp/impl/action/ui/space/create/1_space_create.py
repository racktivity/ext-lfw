from alkira import Alkira

def main(q, i, p, params, tags):
    q.logger.log('Creating space %s' % params['name'], 1)
    alkira = Alkira(p.api)
    space = alkira.createSpace(params['name'],
        params.get("tags", "").split(" "), params.get('repository'),
        params.get('repo_username'), params.get('repo_password'),
        order=params['order'] if params['order'] else 10000)

    params['result'] = space.guid

def match(q, i, p, params, tags):
    return True
