import json

def main(q, i, p, params, tags):
    data = list()
    api = p.application.getAPI('awingu')
    user = api.action.marketplace.user.getObject(params['userguid'])
    capi = i.config.cloudApiConnection.find('main')
    client = q.clients.arakoon.getClient(p.api.appname)
    result = api.action.marketplace.servicesubscription.find(user.customerguid)['result']

    for res in result:
        obj = api.action.marketplace.servicesubscription.getObject(res)
        children = []
        state = 'closed'
        if obj.resourcesprovisioned:
            machine = capi.machine.getObject(obj.resourcesprovisioned['machine'].resourcelist[0].resourceguid)
            resource = json.loads(client.get(str("machine_CU_%s" % machine.guid.lower()))) if client.exists(str("machine_CU_%s" % machine.guid.lower())) else ''
            if resource:
                provider = json.loads(client.get(str("provider_%s_%s" %(resource['resourceprovidertype'], resource['providerguid'])))) if client.exists(str("provider_%s_%s" % (resource['resourceprovidertype'], resource['providerguid']))) else ''
            
            children.append({'data': {'title': machine.name,
                                      'attr': {'href': '/awingu/#/%s/%s?rootobjectguid=%s&providername=%s' % ('sso', 'vmachine_details', machine.guid, provider.get('name',''))}}})
        else:
            state = 'leaf'
        node = {'data': {'title': obj.name,
                         'attr': {'href': '/awingu/#/customers/catalog' }},
                'children': children,
                'state': state}
        data.append(node)
    
    params['result'] = data
