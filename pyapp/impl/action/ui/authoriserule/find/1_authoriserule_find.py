
def main(q, i, p, params, tags):
    filterObject = p.api.model.ui.authoriserule.getFilterObject()
    exact_properties = params['exact_properties'] or ()

    properties = ('groupguids', 'function', 'context')
    for property_name, value in params.iteritems():
        if property_name in properties and not value in (None, ''):
            exact = property_name in exact_properties
            filterObject.add('authoriserule', property_name, value, exactMatch=exact)

    result = p.api.model.ui.authoriserule.find(filterObject)
    params['result'] = result
