

def main(q, i, p, params, tags):
    from pymodel.serializers import ThriftSerializer
    import base64
   
    user = p.api.model.ui.user.get(params['rootobjectguid'])
    # params['result'] = base64.encodestring(space.serialize(ThriftSerializer))
    params['result'] = user
    
def match(q, i, p, params, tags):
	return True
