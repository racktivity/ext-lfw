__tags__ ='osis', 'delete'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    osis = OsisDB().getConnection('main')
    root = q.drp.cloud.get(params['rootobjectguid'])
    osis.viewDelete('page', 'view_page_tag_list', root.guid, root.version)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'page'
