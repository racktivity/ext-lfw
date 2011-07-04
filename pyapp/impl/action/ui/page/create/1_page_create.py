def main(q, i, p, params, tags):
    q.logger.log('Creating page %s/%s' % (params['space'], params['name']), 1)
    alkira = q.clients.alkira.getClientByApi(p.api)
    parent = alkira.getPageByGUID(params["parent"]).name if params['parent'] else None
    alkira.createPage(space=params['space'],
                      name=params['name'],
                      content=params['content'],
                      order=params['order'] if params['order'] else 10000,
                      title=params['title'] if params['title'] else params['name'],
                      tagsList=params.get('tags', '').split(" "),
                      category=params['category'],
                      parent=parent)
                      
    params['result'] = True
    
def match(q, i, p, params, tags):
    return True
