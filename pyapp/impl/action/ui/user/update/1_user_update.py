from alkira import Alkira

def main(q, i, p, params, tags):

    alkira = Alkira(p.api)

    alkira.updateUser(params['userguid'], name=params['name'], password=params['password'])

    params['result'] = user.guid

def match(q, i, p, params, tags):
    return True
