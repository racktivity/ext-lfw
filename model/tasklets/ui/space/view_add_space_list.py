__tags__ ='osis', 'store'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    osis = OsisDB().getConnection('main')
    root = params['rootobject']

    osis.viewSave('ui', 'space', 'view_space_list', root.guid, root.version, {'name': root.name})

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'space' and params['domain'] == 'ui'
