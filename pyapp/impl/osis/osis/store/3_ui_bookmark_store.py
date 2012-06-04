__author__ = 'Racktivity'

from osis.store import OsisConnection

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = OsisConnection.getTableName(domain = params['domain'], objType = params['rootobjecttype'])
    rootobject = params['rootobject']
    values = {
        'name': rootobject.name,
        'url': rootobject.url,
        'order': rootobject.order
    }
    osis.viewSave(params['domain'], params['rootobjecttype'], viewname, rootobject.guid, rootobject.version, values)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'bookmark' and params['domain'] == 'ui'
