def main(q, i, p, params, tags):
    filterObject = p.api.model.ui.authoriserule.getFilterObject()
    exact_properties = params['exact_properties'] or ()

    properties = ('groupguid', 'function', 'context')
    for property_name, value in params.iteritems():
        if property_name in properties and not value in (None, ''):
            exact = property_name in exact_properties
            filterObject.add('ui_view_authoriserule_list', property_name, value, exactMatch=exact)

    result = p.api.model.ui.authoriserule.find(filterObject)
    params['result'] = result
