def main(q, i, p, params, tags):
    alkira = q.clients.alkira.getClientByApi(p.api)
    tags = param.get("tags")
    alkira.updateSpace(params['spaceguid'], params['name'], tags.split(" ") if tags else None,
        order=params['order'] if params['order'] else 10000)
    params['result'] = True

def match(q, i, p, params, tags):
    return True
