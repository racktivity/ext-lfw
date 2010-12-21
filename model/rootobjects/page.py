from osis import model

class page(model.RootObjectModel):
    name = model.String(thrift_id=1)
    space = model.String(thrift_id=2)
    category = model.String(thrift_id=3)
    parent = model.GUID(thrift_id=4)
    tags = model.String(thrift_id=5)
    content = model.String(thrift_id=6)
     
		
