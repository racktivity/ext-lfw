import pymodel as model

#@doc class that provides properties of a authoriserule
class authoriserule(model.RootObjectModel):
    #@doc the groups of the rule
    groupguids = model.List(model.GUID(), thrift_id=1)

    #@doc the function of the rule
    function = model.String(thrift_id=2)

    #@doc the context of the rule
    context = model.Dict(model.String(), thrift_id=3)
