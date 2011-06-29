__tags__ ='osis', 'delete'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    osis = OsisDB().getConnection('main')
    osis.viewDelete('space', 'view_space_tag_list', params['rootobjectguid'], params['rootobjectversionguid'])

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'space' and params['domain'] == 'ui'
