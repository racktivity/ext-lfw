from alkira import Alkira

def main(q, i, p, params, tags):
    alkira = Alkira(p.api)
    alkira.deleteBookmark(params['bookmarkguid'])
    params['result'] = True

def match(q, i, p, params, tags):
    return True
