

def main(q, i, p, params, tags):
    from pymodel.serializers import ThriftSerializer
    import base64

    config = p.api.model.ui.config.get(params['rootobjectguid'])
    # params['result'] = base64.encodestring(page.serialize(ThriftSerializer))
    params['result'] = config

def match(q, i, p, params, tags):
    return True
