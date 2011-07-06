import pymodel as model

#@doc class that provides properties of a page
class config(model.RootObjectModel):
    #@doc space of the config
    space = model.GUID(thrift_id=1)
    #@doc page of the config
    page = model.GUID(thrift_id=2)
    #@doc macro of the config
    macro = model.String(thrift_id=3)
    #@doc id of the config
    configid = model.String(thrift_id=4)
    #@doc data of the config
    data = model.String(thrift_id=5)
    #@doc username of the config
    username = model.String(thrift_id=6)
