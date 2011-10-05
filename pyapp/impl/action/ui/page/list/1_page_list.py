from alkira import Alkira

def main(q, i, p, params, tags):
    alkira = Alkira(p.api)
    result = alkira.listPageInfo(space=params['space'])
    [item.pop('content', None) for item in result]
                    
    params['result'] = result
