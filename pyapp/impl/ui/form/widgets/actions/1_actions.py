import json

TAB_GENERAL_TITLE = 'Actions macro'
TAB_GENERAL_NAME = 'Name : '
TAB_GENERAL_BODY = 'Body : '

def getJsonResult(api, title, body):
    result = json.dumps({'title':title, 'body': body})
    return result

def _getExtraParam(q, params):
    extra = dict()
    if 'extra' in params:
        q.logger.log("Found extra parameter: <%s>" % params["extra"], 4)
        extra = params['extra']
    else:
        q.logger.log("No extra parameter found", 4)

    return extra

def main(q, i, p, params, tags):
    q.logger.log("%s wizard" % TAB_GENERAL_TITLE, level=10)

    extra = _getExtraParam(q, params)

    form = q.gui.form.createForm()

    tab_general = form.addTab('general', TAB_GENERAL_TITLE)

    #define fields of tab
    tab_general.addText(name = '_title',
                        text = TAB_GENERAL_NAME,
                        value = extra['title'] if ('title' in extra) else '')

    tab_general.addText(name = 'body',
                        text = TAB_GENERAL_BODY,
                        multiline = True,
                        value = extra['body'] if ('body' in extra) else '')

    form.loadForm(q.gui.dialog.askForm(form))

    tab_general = form.tabs['general']

    result = getJsonResult(p.api,
                          tab_general.elements['_title'].value,
                          tab_general.elements['body'].value)

    params['result'] = result

def match(q, i, params, tags):
    return True
