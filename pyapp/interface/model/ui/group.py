import pymodel as model

#@doc class that provides properties of a group
class group(model.RootObjectModel):
    #@doc name of the group
    name = model.String(thrift_id=1)

