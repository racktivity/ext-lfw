import json

TAB_GENERAL_TITLE = 'General macro'
TAB_GENERAL_NAME = 'Title : '
TAB_GENERAL_PARAMS = 'Parameters : '
TAB_GENERAL_BODY = 'Body : '

def getJsonResult(api, title, params, body):
    params = params.split("\n")
    paramDict = dict()
    for param in params:
        if not param:
            continue
        if "=" in param:
            key, value = param.split("=")
        elif ":" in param:
            key, value = param.split(":")
        else:
            continue
        paramDict[key.strip()] = value.strip()
    result = json.dumps({'title':title, 'params': paramDict, 'body': body})
    return result

def _getExtraParam(q, params):
    extra = dict()
    if 'extra' in params:
        q.logger.log("Found extra parameter: <%s>" % params["extra"], 4)
        extra = params['extra']
    else:
        q.logger.log("No extra parameter found", 4)

    if 'params' in extra:
        params = extra['params']
        paramsList = list()
        for key in params:
            param = "%s : %s" % (key, params[key])
            paramsList.append(param)
        extra['params'] = "\n".join(paramsList)
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

    tab_general.addText(name = 'params',
                        text = TAB_GENERAL_PARAMS,
                        multiline = True,
                        value = extra['params'] if ('params' in extra) else '')

    tab_general.addText(name = 'body',
                        text = TAB_GENERAL_BODY,
                        multiline = True,
                        value = extra['body'] if ('body' in extra) else '')

    form.loadForm(q.gui.dialog.askForm(form))

    tab_general = form.tabs['general']

    result = getJsonResult(p.api,
                          tab_general.elements['_title'].value,
                          tab_general.elements['params'].value,
                          tab_general.elements['body'].value)

    params['result'] = result

def match(q, i, params, tags):
    return True
