__author__ = "incubaid"

from alkira import Alkira

def main(q, i, p, params, tags):
    macro_tags = params['tags'].tags

    space = macro_tags['space']
    page = macro_tags['page']
    
    alkira = Alkira(p.api)
    breadcrumbs = []
    parent = alkira.getPage(space, page)
    while parent:
        breadcrumbs.append("<a href='#/%(space)s/%(name)s'>%(title)s</a>" % {'space': space,
                                                                           'name': parent.name,
                                                                           'title': parent.title})
        parent = alkira.getPageByGUID(parent.parent) if parent.parent else None
        
    breadcrumbs.reverse()
    
    params['result'] = '/'.join(breadcrumbs)
    