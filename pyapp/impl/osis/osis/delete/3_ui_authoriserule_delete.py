__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    osis.viewDelete(params['domain'], params['rootobjecttype'], params['rootobjecttype'], params['rootobjectguid'])

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'authoriserule' and params['domain'] == 'ui'
