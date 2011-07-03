def main(q, i, p, params, tags):
    alkira = q.clients.alkira.getClientByApi(p.api)
    result = alkira.pageFind(name=params['name'],
                    space=params['space'],
                    category=params['category'],
                    parent=params['parent'],
                    tags=params['tags'],
                    order=params['order'],
                    title=params['title'],
                    exact_properties=params['exact_properties'])
                    
    params['result'] = result
