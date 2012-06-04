__author__ = 'Incubaid'

from osis.store import OsisConnection

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = OsisConnection.getTableName(domain = params['domain'], objType = params['rootobjecttype'])
    rootobject = params['rootobject']
    values = {
        'name': rootobject.name,
        'space': rootobject.space,
        'category': rootobject.category,
        'parent': rootobject.parent,
        'tags': rootobject.tags,
        'order': rootobject.order,
        'title': rootobject.title,
        'pagetype': rootobject.pagetype
    }

    osis.viewSave(params['domain'], params['rootobjecttype'], viewname, rootobject.guid, rootobject.version, values)

    #update global index
    viewname = OsisConnection.getTableName(domain = params['domain'], objType = '_index')
    index = {'name': rootobject.title if rootobject.title else rootobject.name,
             'url': 'page://%s/%s' % (p.api.model.ui.space.get(rootobject.space).name, rootobject.name),
             'content': rootobject.content,
             'tags': rootobject.tags,
             'description': rootobject.description}
    
    osis.viewSave(params['domain'], '_index', viewname, rootobject.guid, rootobject.version, index)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'page' and params['domain'] =='ui'
