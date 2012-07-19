__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    rootobject = params['rootobject']
    values = {
        'space': rootobject.space,
        'page': rootobject.page,
        'macro': rootobject.macro,
        'configid': rootobject.configid,
        'data': rootobject.data,
        'username': rootobject.username
    }
    osis.viewSave(params['domain'], params['rootobjecttype'], params['rootobjecttype'], rootobject.guid, rootobject.version, values)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'config' and params['domain'] =='ui'
