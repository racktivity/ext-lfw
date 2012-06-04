from osis.store import OsisConnection

def main(q, i, p, params, tags):
    bookmarkTable = OsisConnection.getTableName(domain = 'ui', objType = 'bookmark')
    filterObject = p.api.model.ui.bookmark.getFilterObject()
    exact_properties = params['exact_properties'] or ()

    properties = ('name')
    for property_name, value in params.iteritems():
        if property_name in properties and not value in (None, ''):
            exact = property_name in exact_properties
            filterObject.add(bookmarkTable, property_name, value, exactMatch=exact)

    result = p.api.model.ui.bookmark.find(filterObject)
    params['result'] = result
