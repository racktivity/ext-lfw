import pymodel as model

#@doc class that provides properties of a space
class project(model.RootObjectModel):
    #@doc name of the project
    name = model.String(thrift_id=1)
    #@doc project path
    path = model.String(thrift_id=2)
    #@doc tags related to the project
    tags = model.String(thrift_id=3)
