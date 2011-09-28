def main(q, i, params, service, job, tags, tasklet):
    print '>>> Space: %s, Name: %s, Content: %s' % (params.space, params.name, params.content)
    service.extensions.pages.createPage(service, params.space, params.name, params.content)
    params.result = True
    return params

def match(q, i, params, service, job, tags, tasklet):
    return True
