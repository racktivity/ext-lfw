def main(q, i, params, service, job, tags, tasklet):
    service.extensions.pages.deletePage(service, params.space, params.name)
    params.result = True
    return params

def match(q, i, params, service, job, tags, tasklet):
    return True
