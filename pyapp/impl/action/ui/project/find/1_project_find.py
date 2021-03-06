
def main(q, i, p, params, tags):
    filterObject = p.api.model.ui.project.getFilterObject()
    exact_properties = params['exact_properties'] or ()

    properties = ('name', 'tags')
    for property_name, value in params.iteritems():
        if property_name in properties and not value in (None, ''):
            exact = property_name in exact_properties
            filterObject.add('project', property_name, value, exactMatch=exact)

    result = p.api.model.ui.project.find(filterObject)
    params['result'] = result
