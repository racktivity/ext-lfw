

def main(q, i, p, params, tags):
    from pymodel.serializers import ThriftSerializer
    import base64
   
    project = p.api.model.ui.project.get(params['rootobjectguid'])
    # params['result'] = base64.encodestring(space.serialize(ThriftSerializer))
    params['result'] = project
    
def match(q, i, p, params, tags):
	return True
