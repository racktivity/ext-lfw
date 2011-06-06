__author__ = "incubaid"

def main(q, i, p, params, tags):
    macro_tags = params['tags'].tags

    space = macro_tags['space']
    depth = int(macro_tags['depth'])
    root_page = macro_tags.get('root', 'self')

    appname = p.api.appname
    alkira_client = q.clients.alkira.getClient('127.0.0.1', appname)

    all_pages_info = alkira_client.listPageInfo(space)
    all_pages_info = filter(lambda x: x['name'] != 'pagetree', all_pages_info)

    page_guid_dict = dict( [ (x['name'], x['guid']) for x in all_pages_info ] )
    page_parent_dict = dict( [ (x['name'], x['parent']) for x in all_pages_info ] )

    all_pages = []
    for i in all_pages_info:
        all_pages.append(i['name'])
    all_pages.sort()

    root_pages = []
    if root_page != 'self':
        root_pages.append(root_page)
    else:
        root_pages = [ x['name'] for x in all_pages_info if not x['parent'] ]

    def getGuid(page_name):
        return page_guid_dict.get(page_name)

    def getParent(page_name):
        return page_parent_dict.get(page_name)

    def childPages(root, pages, tree, tree_depth):
        tree_depth -= 1
        children = {}
        root_guid = getGuid(root)

        for page in pages:
            page_parent = getParent(page)
            if root_guid == page_parent:
                children.update({page:{}})
        tree[root].update(children)
        if  tree_depth > 0:
            for child in tree[root].keys():
                childPages(child, all_pages, tree[root], tree_depth)
        return tree

    values = []
    for each_root_page in root_pages:
        values.append(childPages(each_root_page, all_pages, {each_root_page:{}}, depth))

    global children_str
    children_str = ""

    def treePrint(indent, value_dict):
        if value_dict:
            for item in value_dict:
                global children_str
                page_name = item.replace("_", "\_")
                children_str += indent*' ' + "* <a href='/" + appname + '/#/' + space + '/' + item + "'>" + page_name + '</a>  \n'
                treePrint(indent+4, value_dict[item])

    values.sort()
    for each_value in values:
        treePrint(0, each_value)

    if (root_page != 'self') and (root_page not in all_pages):
        children_str = 'Page "%s" does not exist.'%root_page

    result = """
%s
- - -
    """%(children_str)
    params['result'] = result 
