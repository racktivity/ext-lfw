__author__ = "incubaid"

from alkira import Alkira

def main(q, i, p, params, tags):
    macro_tags = params['tags'].tags

    space = macro_tags['space']
    page = macro_tags['page']
    depth = int(macro_tags.get('depth', '1'))
    root_page = macro_tags.get('root', page)

    appname = p.api.appname
    alkira_client = Alkira(p.api)

    all_pages_info = alkira_client.listPageInfo(space)
    all_pages_info = filter(lambda x: x['name'] != 'pagetree', all_pages_info)

    page_guid_dict = dict( [ (x['name'], x['guid']) for x in all_pages_info ] )
    page_parent_dict = dict( [ (x['name'], x['parent']) for x in all_pages_info ] )
    page_title_dict = dict( [ (x['name'], x['title']) for x in all_pages_info ] )
    page_order_dict = dict( [ (x['name'], x['order']) for x in all_pages_info ] )

    all_pages = [x['name'] for x in all_pages_info]

    if root_page != 'all':
        root_pages = [root_page]
    else:
        root_pages = [ x['name'] for x in all_pages_info if not x['parent'] ]

    if (root_page != 'all') and (root_page not in all_pages):
        children_str = 'Page "%s" does not exist.'%root_page

    def getGuid(page_name):
        return page_guid_dict.get(page_name)

    def getParent(page_name):
        return page_parent_dict.get(page_name)

    def getTitle(page_name):
        return page_title_dict.get(page_name)

    def childPages(root, pages, tree, tree_depth):
        tree_depth -= 1
        children = {}
        root_guid = getGuid(root)

        for page in pages:
            page_parent = getParent(page)
            if root_guid == page_parent:
                children[page] = {}
        tree[root] = children
        if  tree_depth > 0:
            for child in tree[root].keys():
                childPages(child, all_pages, tree[root], tree_depth)
        return tree

    values = []
    for each_root_page in root_pages:
        values.append(childPages(each_root_page, all_pages, {each_root_page:{}}, depth))

    global children_str
    children_str = ""
    
    def pageSorter(page1, page2):
        result = cmp(page_order_dict[page1], page_order_dict[page2])
        if result == 0:
            return cmp(page1, page2)
        else:
            return result

    def treePrint(indent, value_dict, hide):
        if value_dict:
            for item in sorted(value_dict, cmp=pageSorter):
                if hide == True:
                    treePrint(0, value_dict[item], False)
                else:
                    global children_str
                    page_title = getTitle(item).replace("_", "\_")
                    children_str += indent*' ' + "* <a href='/" + appname + '/#/' + space + '/' + item + "'>" + page_title + '</a>  \n'
                    treePrint(indent+4, value_dict[item], False)

    for each_value in values:
        if root_page == 'all':
            treePrint(0, each_value, False)
        else:
            treePrint(0, each_value, True)

    result = """
%s
- - -
    """%(children_str)
    params['result'] = result 
