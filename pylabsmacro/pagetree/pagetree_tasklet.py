import sqlalchemy

def main(q, i, p, params, tags): #pylint: disable=W0613
    def makeNode(title, href='', children=list(), state='leaf'):
        node = {
            'data': {
                'title': title,
                'attr': { 'href': href }
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
    spaceNames = params['space'].split(',')
    _id = params['id']
    lazyload = params['lazyload']

    page = service.alkira.osis.findTable("ui", "page")
    space = service.alkira.osis.findTable("ui", "space")

    columns = [ page.c.guid.label("guid"), page.c.parent.label("parent"), page.c.name.label("name"),
        page.c.title.label("title"), page.c.order.label("order"), space.c.order.label("spaceorder"),
        space.c.name.label("spacename") ]
    join = [ page.join(space, page.c.space == space.c.guid) ]
    where = [ space.c.name.in_(spaceNames) ]
    order = [ space.c.order.asc(), page.c.order.asc(), page.c.title.asc() ]

    if lazyload:
        localpage = page.alias("localpage")
        columns.append(
            sqlalchemy.select([ sqlalchemy.func.count(localpage.c.guid) ]).where(localpage.c.parent == page.c.guid).label("nrofkids")
        )

        if _id == 0:
            where.append(page.c.parent == None)
        elif q.basetype.guid.check(_id):
            where.append(page.c.parent == _id)
        else:
            parentselect = sqlalchemy.select([ page.c.guid ], distinct=True, from_obj=join,
                whereclause=[ space.c.name.in_(spaceNames), page.c.name == _id ], order_by=order)
            result = service.alkira.osis.runSqlAlchemyQuery(parentselect).fetchone()
            where.append(page.c.parent == result[0])

    select = sqlalchemy.select(columns, distinct=True, from_obj=join, whereclause=sqlalchemy.and_(*where), order_by=order)

    result = service.alkira.osis.runSqlAlchemyQuery(select)

    data = list()
    if not lazyload:
        parents = dict()
        rootnodes = list()
        nodesmap = dict()
        for node in result:
            node = dict(node)
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
            nodedata = makeNode(rootnode['title'], '#/%s/%s' % (rootnode['spacename'], rootnode['name']), childnodes)
            data.append(nodedata)

    else:
        for node in result :
            node = dict(node)
            if node['name'] == 'pagetree':
                continue
            nodedata = dict()
            state = 'closed' if 'nrofkids' in node and node['nrofkids'] > 0 else 'leaf'
            nodedata = {
                'data': {
                    'title': node['title'],
                    'type': 'link',
                    'attr': {
                        'href': '#/%s/%s' % (node['spacename'], node['name'])
                    },
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

