from alkira import Alkira

def main(q, i, p, params, tags):
    alkira = Alkira(p.api)
    alkira.deletePageByGUID(params['pageguid'])
    params['result'] = True
    
def match(q, i, p, params, tags):
    return True
