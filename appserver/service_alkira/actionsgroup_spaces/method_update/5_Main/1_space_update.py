def main(q, i, params, service,job,tags, tasklet):
    q.logger.log('Update space with name %s to new name %s' % (params.name,
            params.newName), 3)
    service.extensions.spaces.update(service, params.name, params.newName, params.tags)
    params.result = True
    return params

def match(q, i, params, service,job,tags, tasklet):
    return True
