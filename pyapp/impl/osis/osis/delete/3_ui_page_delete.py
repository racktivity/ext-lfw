__author__ = 'Incubaid'

from osis.store import OsisConnection

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname) 
    viewname = OsisConnection.getTableName(domain = params['domain'], objType = params['rootobjecttype'])
    osis.viewDelete(params['domain'], params['rootobjecttype'], viewname, params['rootobjectguid'])
    
    #clear index.
    osis.viewDelete(params['domain'], '_index', '_index', params['rootobjectguid'])

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'page' and params['domain'] == 'ui'
