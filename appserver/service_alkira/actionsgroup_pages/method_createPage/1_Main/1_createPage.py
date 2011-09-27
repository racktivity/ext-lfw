def main(q, i, params, service, job, tags, tasklet):
    print '>>> Space: %s, Name: %s, Content: %s' % (params.space, params.name, params.content)
    page_id = '%s:%s' % (params.space, params.name)
    service.db.set(key=page_id, value=params.content)
    params.result = True
    return params

def match(q, i, params, service, job, tags, tasklet):
    return True

