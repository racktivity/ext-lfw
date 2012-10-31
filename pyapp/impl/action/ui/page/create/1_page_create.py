from alkira import Alkira

def main(q, i, p, params, tags):
    q.logger.log('Creating page %s/%s' % (params['space'], params['name']), 1)
    alkira = Alkira(p.api)
    parent = alkira.getPageByGUID(params["parent"]).name if params['parent'] else None
    for key in params:
        if type(params[key]) == unicode:
            params[key] = params[key].encode('utf-8')
    page = alkira.createPage(space=params['space'],
                      name=params['name'],
                      content=params['content'],
                      order=params['order'] if params['order'] else 10000,
                      title=params['title'] if params['title'] else params['name'],
                      tagsList=params.get('tags', '').split(" ") if params['tags'] else [],
                      category=params['category'],
                      parent=parent,
                      description=params['description'])
    if page:
        params['result'] = page.guid
    else:
        params['result'] = None

def match(q, i, p, params, tags):
    return True
