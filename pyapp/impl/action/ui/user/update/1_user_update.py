from alkira import Alkira

def main(q, i, p, params, tags):

    alkira = Alkira(p.api)
    user = alkira.getPageByGUID(params['userguid'])

    alkira.updateUser(name=params['name'],
                      password=params['password'],
                      tagsList=params.get('tags', '').split(" "))

    params['result'] = user.guid
    
def match(q, i, p, params, tags):
    return True
