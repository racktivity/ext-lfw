def main(q, i, params, service,job,tags, tasklet):
    q.logger.log('List spaces', 3)
    spaces = service.extensions.spaces.list(service)
    params.result = spaces
    return params


def match(q, i, params, service,job,tags, tasklet):
    return True
