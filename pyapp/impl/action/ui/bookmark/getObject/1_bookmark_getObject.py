def main(q, i, p, params, tags):
    bookmark = p.api.model.ui.bookmark.get(params['rootobjectguid'])
    params['result'] = bookmark

def match(q, i, p, params, tags):
    return True
