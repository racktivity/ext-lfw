__author__ = 'Incubaid'

import string
from alkira.serialize import json_print_dict
from osis.store import OsisConnection

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = OsisConnection.getTableName(domain = params['domain'], objType = params['rootobjecttype'])
    rootobject = params['rootobject']
    values = {
        'groupguids': ";" + string.join(rootobject.groupguids, ";") + ";" if rootobject.groupguids else "",
        'function': rootobject.function,
        'context': json_print_dict(rootobject.context._dict)
    }
    osis.viewSave(params['domain'], params['rootobjecttype'], viewname, rootobject.guid, rootobject.version, values)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'authoriserule' and params['domain'] == 'ui'
