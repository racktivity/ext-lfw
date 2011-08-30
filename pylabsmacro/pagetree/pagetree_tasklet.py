def main(q, i, p, params, tags):

    def makeNode(title, href='', children=[], state='leaf'):
        node = { 'data': {'title': title,
                          'attr': {'href': href}  
                         },
                 'children': children,
                 'state': state
        }
        return node

    def _constructChildren(parents, guid, spacename, nodesmap):
        if guid not in parents:
            return list()
        if not parents[guid]:
            return list()
        children = list()
        for childguid in parents[guid]:
            child = nodesmap[childguid]
            childnode = makeNode(child['title'], '#/%s/%s' % (spacename, child['name']), _constructChildren(parents, childguid, spacename, nodesmap))
            children.append(childnode)
        return children


    service = params['service']
    space = params['space']
    id = params['id']
    lazyload = params['lazyload']

    space = service.alkira.getSpace(space)
    where = ""
    if id == 0:
        where = "and pagelist.parent is null"
    elif q.basetype.guid.check(id):
        where = "and pagelist.parent = '%s'" % id
    else:
        sql1 = """
            SELECT DISTINCT pagelist.guid
            FROM ONLY ui_page.ui_view_page_list as pagelist
            WHERE pagelist.space ='%(space)s' and pagelist.name = '%(id)s';
            """ % {'space': space.guid, 'id': id}

        parent_guid_result = service.connection.page.query(sql1)
        parent_guid = parent_guid_result[0]['guid']
        where = "and pagelist.parent = '%s'" % parent_guid

    if not lazyload:
        sql = """
        SELECT DISTINCT pagelist.guid,
            pagelist.parent,
            pagelist.name,
            pagelist.title,
            pagelist.order
            FROM ONLY ui_page.ui_view_page_list as pagelist
            WHERE pagelist.space = '%(space)s'
            ORDER BY pagelist.order, pagelist.title;
        """ % {'space': space.guid}
    else:
        sql = """
        SELECT DISTINCT pagelist.guid,
                pagelist.parent,
                pagelist.name,
                pagelist.title,
                pagelist.order,
                (select count(guid) FROM ui_page.ui_view_page_list WHERE ui_page.ui_view_page_list.parent = pagelist.guid) as nrofkids
                FROM ONLY ui_page.ui_view_page_list as pagelist
                WHERE pagelist.space = '%(space)s' %(where)s ORDER BY pagelist.order, pagelist.title;
        """ % {'space': space.guid, 'where': where}

    result = service.connection.page.query(sql)
    data = list()
    if not lazyload:
        parents = dict()
        rootnodes = list()
        nodesmap = dict()
        for node in result:
            if node['name'] == 'pagetree':
                continue
            if not node['parent']:
                rootnodes.append(node)
            else:
                #construct parents dict
                parents.setdefault(node['parent'], list()).append(node['guid'])
            nodesmap[node['guid']] = node

        #Get child nodes of each parent
        for rootnode in rootnodes:
            childnodes = _constructChildren(parents, rootnode['guid'], space.name, nodesmap)
            nodedata = makeNode(rootnode['title'], '#/%s/%s' % (space.name, node['name']), childnodes)
            data.append(nodedata)
        
    else:
        for node in result :
            if node['name'] == 'pagetree':
                continue
            nodedata = dict()
            children = list()
            state = 'closed' if 'nrofkids' in node and node['nrofkids'] > 0 else 'leaf'
            nodedata = {'data': {'title': node['title'],
                                 'type': 'link',
                                 'attr': {'href': '#/%s/%s' % (space.name, node['name'])},
                                 'children':[]
                                 },
                        'attr': {
                                 'class': 'TreeTitle',
                                 'id': node['guid']
                                },
                        'state' : state
                        }
            data.append(nodedata)
    q.logger.log(data, 1)
    params['result'] = data

