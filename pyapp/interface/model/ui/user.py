import pymodel as model

#@doc class that provides properties of a user
class user(model.RootObjectModel):
    #@doc name of the user
    name = model.String(thrift_id=1)
    #@doc tags related to the user
    tags = model.String(thrift_id=2)
    #@doc list of user spaces
    spaces = model.List(model.String(), thrift_id=3)
    #@doc list of user pages
    pages = model.List(model.String(), thrift_id=4)
    #@doc password for the user
    password = model.String(thrift_id=5)
