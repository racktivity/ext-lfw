def main(q, i, params, service, job, tags, tasklet):
    space = getattr(params, 'space', None)
    params.result = service.extensions.pages.countPages(service, space)
    return params

def match(q, i, params, service, job, tags, tasklet):
    return True
