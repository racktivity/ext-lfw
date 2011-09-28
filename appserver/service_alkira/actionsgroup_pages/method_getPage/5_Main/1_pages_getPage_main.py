def main(q, i, params, service, job, tags, tasklet):
    params.result = service.extensions.pages.getPage(service, params.space, params.name)
    return params

def match(q, i, params, service, job, tags, tasklet):
    return True
