

def main(q, i, p, params, tags):
    from pymodel.serializers import ThriftSerializer
    import base64

    group = p.api.model.ui.group.get(params['rootobjectguid'])
    # params['result'] = base64.encodestring(group.serialize(ThriftSerializer))
    params['result'] = group

def match(q, i, p, params, tags):
    return True
