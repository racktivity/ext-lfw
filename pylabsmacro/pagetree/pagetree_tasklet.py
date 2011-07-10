def main(q, i, p, params, tags):
    service = params['service']
    space = params['space']
    id = params['id']

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
    for node in result :
        if node['name'] == 'pagetree':
            continue
        nodedata = dict()
        children = list()
        state = 'closed' if node['nrofkids'] > 0 else 'leaf'
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

