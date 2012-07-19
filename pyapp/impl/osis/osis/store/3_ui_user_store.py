__author__ = 'Incubaid'

import string

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    rootobject = params['rootobject']
    values = {
        'name': rootobject.name,
        'login': rootobject.login,
        'groupguids': ";" + string.join(rootobject.groups, ";") + ";" if rootobject.groups else ""
    }
    osis.viewSave(params['domain'], params['rootobjecttype'], params['rootobjecttype'], rootobject.guid, rootobject.version, values)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'user' and params['domain'] == 'ui'
