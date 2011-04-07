from pylabs import q


class WidgetService():

    def __init__(self):
        tasklet_path = q.system.fs.joinPaths(q.system.fs.getDirName(__file__),"tasklets")
        self.tasklet_engine = q.getTaskletEngine(tasklet_path)
    @q.manage.applicationserver.expose
    def getWidgetConfig(self, widget_id, space="", pagename="", parentwidget_id="",  widget_type=""):
        params = {'pagename':pagename, 'space': space, 'parentwidget_id': parentwidget_id, 'widget_type': widget_type, 'widget_id': widget_id}
        self.tasklet_engine.execute(params=params, tags=('widget', 'get'))
        return params['result']
        
    @q.manage.applicationserver.expose
    def setWidgetConfig(self, widget_id, widget_config, space="", pagename="", parentwidget_id="", widget_type=""):
        params = {'space': space, 'pagename': pagename, 'parentwidget_id': parentwidget_id, 'widget_type': widget_type, 'widget_id': widget_id, 'widget_config': widget_config}
        self.tasklet_engine.execute(params=params, tags=('widget', 'set'))
        return params['result']

    @q.manage.applicationserver.expose
    def generic(self, tagstring=None):
        q.logger.log('[GENERIC]: Got req: ts="%s"' % tagstring, 1)

	tags = q.base.tags.getObject(tagstring)
 
	params = {'tags': tags}
        self.tasklet_engine.execute(params=params, tags=['macro', 'generic'])

        q.logger.log('[GENERIC]: Result: "%s"' % params.get('result', ''), 1)

        return params.get('result', '')


