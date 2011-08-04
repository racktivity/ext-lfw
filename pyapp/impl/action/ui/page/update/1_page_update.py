from alkira import Alkira

def main(q, i, p, params, tags):

    alkira = Alkira(p.api)
    page = alkira.getPageByGUID(params['pageguid'])
    parent = alkira.getPageByGUID(params["parent"]).name if params['parent'] else None
    
    alkira.updatePage(space=page.space,
                      old_name=page.name,
                      name=params['name'],
                      content=params['content'],
                      order=params['order'] if params['order'] else 10000,
                      title=params['title'] if params['title'] else params['name'],
                      tagsList=params.get('tags', '').split(" ") if params['tags'] else None,
                      category=params['category'],
                      parent=parent)
                      
    params['result'] = True
    
def match(q, i, p, params, tags):
    return True
