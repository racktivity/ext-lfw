from osis.store import OsisConnection

def main(q, i, p, params, tags):
    groupTable = OsisConnection.getTableName(domain = 'ui', objType = 'group')
    filterObject = p.api.model.ui.group.getFilterObject()
    exact_properties = params['exact_properties'] or ()

    properties = ('name')
    for property_name, value in params.iteritems():
        if property_name in properties and not value in (None, ''):
            exact = property_name in exact_properties
            filterObject.add(groupTable, property_name, value, exactMatch=exact)

    result = p.api.model.ui.group.find(filterObject)
    params['result'] = result
