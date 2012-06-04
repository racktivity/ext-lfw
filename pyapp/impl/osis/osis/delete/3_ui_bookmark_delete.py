__author__ = 'Racktivity'

from osis.store import OsisConnection

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = OsisConnection.getTableName(domain = params['domain'], objType = params['rootobjecttype'])
    osis.viewDelete(params['domain'], params['rootobjecttype'], viewname, params['rootobjectguid'])

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'bookmark' and params['domain'] == 'ui'
