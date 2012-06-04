from osis.store import OsisConnection

def main(q, i, p, params, tags):
    projectTable = OsisConnection.getTableName(domain = 'ui', objType = 'project')
    filterObject = p.api.model.ui.project.getFilterObject()
    exact_properties = params['exact_properties'] or ()



    properties = ('name', 'tags')
    for property_name, value in params.iteritems():
        if property_name in properties and not value in (None, ''):
            exact = property_name in exact_properties
            filterObject.add(projectTable, property_name, value, exactMatch=exact)

    result = p.api.model.ui.project.find(filterObject)
    params['result'] = result
