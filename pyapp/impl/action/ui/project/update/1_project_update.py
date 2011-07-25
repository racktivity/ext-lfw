from alkira import Alkira

def main(q, i, p, params, tags):
    alkira = Alkira(p.api)
    tags = params.get("tags")
    alkira.updateProject(params['projectguid'],
                         newname=params['name'],
                         path=params['path'],
                         tagsList=tags.split(" ") if tags else None)
    
    params['result'] = True

def match(q, i, p, params, tags):
    return True
