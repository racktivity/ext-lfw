import json

TAB_GENERAL_TITLE = 'Table of Contents macro'
TAB_GENERAL_NAME = 'Name : '

def getJsonResult(api, title):
    result = json.dumps({'title':title})
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
                        value = extra['name'] if ('name' in extra) else '')

    form.loadForm(q.gui.dialog.askForm(form))

    tab_general = form.tabs['general']

    result = getJsonResult(p.api,
                          tab_general.elements['_title'].value)

    params['result'] = result

def match(q, i, params, tags):
    return True