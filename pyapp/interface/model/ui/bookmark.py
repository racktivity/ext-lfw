import pymodel as model

#@doc class that provides properties of a bookmark
class bookmark(model.RootObjectModel):
    #@doc name of the bookmark
    name = model.String(thrift_id=1)
    #@doc url the bookmark points to
    url = model.String(thrift_id=2)
    #@doc the order of the bookmark
    order = model.Integer(thrift_id=3)
