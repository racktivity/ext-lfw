

def main(q, i, p, params, tags):
    from pymodel.serializers import ThriftSerializer
    import base64
   
    space = p.api.model.ui.space.get(params['rootobjectguid'])
    # params['result'] = base64.encodestring(space.serialize(ThriftSerializer))
    params['result'] = space
    
def match(q, i, p, params, tags):
	return True
