from alkira import Alkira

def main(q, i, p, params, tags):
    alkira = Alkira(p.api)
    alkira.deleteUserFromGroup(userguid=params['userguid'], groupguid=params['groupguid'])
    params['result'] = True

def match(q, i, p, params, tags):
    return True
