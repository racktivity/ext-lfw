from alkira import Alkira

def main(q, i, p, params, tags):
    alkira = Alkira(p.api)
    alkira.updateBookmark(params['bookmarkguid'], name=params['name'], url=params['url'], order=params['order'])

    params['result'] = True

def match(q, i, p, params, tags):
    return True
