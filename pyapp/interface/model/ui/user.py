import pymodel as model

#@doc class that provides properties of a user
class user(model.RootObjectModel):
    #@doc name of the user
    name = model.String(thrift_id=1)

    #@doc groups of which the user is a member of
    groups = model.List(model.GUID(), thrift_id=2)
