def main(q, i, params, service,job,tags, tasklet):
    q.logger.log('Create space with name %s' % params.name, 3)
    service.extensions.spaces.create(service, params.name)
    params.result = True
    return params

def match(q, i, params, service,job,tags, tasklet):
    return True
