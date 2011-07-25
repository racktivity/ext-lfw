from alkira import Alkira

def main(q, i, p, params, tags):
    q.logger.log('Creating space %s' % params['name'], 1)
    alkira = Alkira(p.api)
    alkira.createProject(params['name'],
                         params['path'],
                         tagsList=params.get("tags", "").split(" "))

    params['result'] = True

def match(q, i, p, params, tags):
    return True
