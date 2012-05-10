

def main(q, i, p, params, tags):
    from pymodel.serializers import ThriftSerializer
    import base64

    authoriserule = p.api.model.ui.authoriserule.get(params['rootobjectguid'])
    # params['result'] = base64.encodestring(authoriserule.serialize(ThriftSerializer))
    params['result'] = authoriserule

def match(q, i, p, params, tags):
    return True
