__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname) 
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    rootobject = params['rootobject']
    values = {
        'name': rootobject.name,
        'space': rootobject.space,
        'category': rootobject.category,
        'parent': rootobject.parent,
        'tags': rootobject.tags,
        'content': rootobject.content,
        'order': rootobject.order,
        'title': rootobject.title
    }
    osis.viewSave(params['domain'], params['rootobjecttype'], viewname, rootobject.guid, rootobject.version, values)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'page' and params['domain'] =='ui'
