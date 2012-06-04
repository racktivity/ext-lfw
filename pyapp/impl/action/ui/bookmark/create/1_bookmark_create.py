from alkira import Alkira

def main(q, i, p, params, tags):
    q.logger.log('Creating bookmark %s - %s' % (params['name'], params['url']), 1)
    alkira = Alkira(p.api)
    alkira.createBookmark(params['name'], params['url'], params['order'])
    params['result'] = True

def match(q, i, p, params, tags):
    return True
