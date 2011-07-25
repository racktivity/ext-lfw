__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname) 
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    osis.viewDelete(params['domain'], params['rootobjecttype'], viewname, params['rootobjectguid'])
    
    #clear index.
    osis.viewDelete(params['domain'], '_index', 'global_index_view', params['rootobjectguid'])

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'page' and params['domain'] == 'ui'
