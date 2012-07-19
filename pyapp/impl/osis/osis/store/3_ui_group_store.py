__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    rootobject = params['rootobject']
    values = {
        'name': rootobject.name
    }
    osis.viewSave(params['domain'], params['rootobjecttype'], params['rootobjecttype'], rootobject.guid, rootobject.version, values)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'group' and params['domain'] == 'ui'
