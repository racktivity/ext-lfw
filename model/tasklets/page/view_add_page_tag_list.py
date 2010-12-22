__tags__ ='osis', 'store'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    osis = OsisDB().getConnection('main')
    root = params['rootobject']
  
    if root.tags:  
        fields = [{'tag': tag} for tag in root.tags.split(' ') if tag]
        osis.viewSave('page', 'view_page_tag_list', root.guid, root.version, fields)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'page'
