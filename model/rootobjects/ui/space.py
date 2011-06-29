from osis import model

class page(model.RootObjectModel):
    name = model.String(thrift_id=1)
    tags = model.String(thrift_id=2)
