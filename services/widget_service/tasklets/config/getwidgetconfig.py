__author__ = "racktivity"
__tags__ = 'widget', 'get'

def main(q, i, params, tags):
    arakoonclient = q.clients.arakoon.getClient()

    key = '.'.join([params['space'], params['pagename'], params['widget_type'], params['widget_id']])

    key = key.lower()

    q.logger.log('KEY: %s' % key, 1)

    import json 

    if arakoonclient.exists(key):
         params['result'] = json.loads(arakoonclient.get(key))
    else:
       params['result'] = {'name':'testwidget', 'positionx':'20', 'positiony':'40'} 

def match(q,i, params,tags):
    #check widget type, ... for a specific handling of th widget
    return True
