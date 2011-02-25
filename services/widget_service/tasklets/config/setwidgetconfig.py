__author__ = "racktivity"
__tags__ = 'widget', 'set'

def main(q, i, params, tags):
    arakoonclient = q.clients.arakoon.getClient()
    arakoonclient.set(params['widget_id'], params['widget_config'])
    params['result'] = 0
 

def match(q,i, params,tags):
    #check widget type, ... for a specific handling of th widget
    return True
