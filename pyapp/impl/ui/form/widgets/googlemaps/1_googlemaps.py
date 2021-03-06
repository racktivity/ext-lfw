import json

TAB_GENERAL_TITLE = 'Google maps macro'
TAB_GENERAL_NAME = 'Title : '
TAB_GENERAL_PARAMS = {
    'longitude':{
                    'question' : 'Longitude : ',
                    'key': 'longitude',
                    'type': 'string',
                    'helpText': 'Longitude on earth'
                },
    'lattitude':    {
                    'question' : 'Lattitude : ',
                    'key': 'lattitude',
                    'type': 'string',
                    'helpText': 'Lattitude on earth'
                },
    'width':     {
                    'question' : 'Width : ',
                    'key': 'width',
                    'type': 'int',
                    'helpText': 'Width of the canvas'
                },
    'height':     {
                    'question' : 'Height : ',
                    'key': 'height',
                    'type': 'int',
                    'helpText': 'Height of the canvas'
                },
    'zoom':     {
                    'question' : 'Zoom level : ',
                    'key': 'appname',
                    'type': 'int',
                    'helpText': 'Zoomlevel of the map'
                }
}

def getJsonResult(api, title, tab_general):
    params = dict()
    for key in TAB_GENERAL_PARAMS:
        fieldKey = TAB_GENERAL_PARAMS[key]['key']
        if not fieldKey in tab_general.elements:
            continue
        value = tab_general.elements[fieldKey].value
        params[key] = value

    result = json.dumps({'title': title, 'params': params})
    return result

def _addParamsFields(tab_general, extra):
    for key in TAB_GENERAL_PARAMS:
        fieldKey = TAB_GENERAL_PARAMS[key]['key']
        defaultValue = helpText = ''
        if 'params' in extra:
            if key in extra['params']:
                defaultValue = extra['params'][key]
        if 'helpText' in TAB_GENERAL_PARAMS[key]:
            helpText = TAB_GENERAL_PARAMS[key]['helpText']

        if TAB_GENERAL_PARAMS[key]['type'] == 'string':
            tab_general.addText(name = fieldKey,
                    text = TAB_GENERAL_PARAMS[key]['question'],
                    value = defaultValue, helpText = helpText)
        elif TAB_GENERAL_PARAMS[key]['type'] == 'int':
            tab_general.addInteger(name = fieldKey,
                    text = TAB_GENERAL_PARAMS[key]['question'],
                    value = defaultValue, helpText = helpText)

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

    _addParamsFields(tab_general, extra)

    form.loadForm(q.gui.dialog.askForm(form))

    tab_general = form.tabs['general']

    result = getJsonResult(p.api,
                          tab_general.elements['_title'].value, tab_general)

    params['result'] = result

def match(q, i, params, tags):
    return True
