__author__ = 'Racktivity'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    rootobject = params['rootobject']
    values = {
        'name': rootobject.name,
        'url': rootobject.url,
        'order': rootobject.order
    }
    osis.viewSave(params['domain'], params['rootobjecttype'], params['rootobjecttype'], rootobject.guid, rootobject.version, values)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'bookmark' and params['domain'] == 'ui'
