from alkira import Alkira

def main(q, i, p, params, tags):

    alkira = Alkira(p.api)

    params['result'] = alkira.updateUser(params['userguid'], name=params['name'], password=params['password'])

def match(q, i, p, params, tags):
    return True
