__tags__ ='osis', 'store'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    osis = OsisDB().getConnection('main')
    root = params['rootobject']

    osis.viewSave('page', 'view_page_list', root.guid, root.version, 
                    {'name'                  :root.name, 
                     'space'                 :root.space, 
                     'category'              :root.category, 
                     'parent'                :root.parent, 
                     'content'               :root.content})

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'page'
