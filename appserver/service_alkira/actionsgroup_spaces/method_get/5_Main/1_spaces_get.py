def main(q, i, params, service,job,tags, tasklet):
    q.logger.log('Getting space with name %s' % params.name, 3)
    result = service.extensions.spaces.get(service, params.name)
    params.result = result
    return params

def match(q, i, params, service,job,tags, tasklet):
    return True
