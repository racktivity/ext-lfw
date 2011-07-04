import json

TAB_GENERAL_TITLE = 'Wizard macro'
TAB_GENERAL_NAME = 'Title : '
TAB_GENERAL_PARAMS = {
    'appserver':{
                    'question' : 'Application server name : ',
                    'key': 'appserver',
                    'type': 'string',
                    'helpText': 'Name of the application server that runs the wizard, by default the application server of the domain of your document'
                },
    'title':    {
                    'question' : 'Title : ',
                    'key': '__title',
                    'type': 'string',
                    'helpText': 'Title for your wizard, as it will appear in your document'
                },
    'name':     {
                    'question' : 'Name : ',
                    'key': '__name',
                    'type': 'string',
                    'helpText': 'Name of the wizard, must be the name of the directory in which the desired wizard is located'
                },
    'type':     {
                    'question' : 'Type : ',
                    'key': 'type',
                    'type': 'string',
                    'helpText': 'Type of element in your document, either button (by default) or link'
                },
    'appname':  {
                    'question' : 'Application Name : ',
                    'key': 'appname',
                    'type': 'string',
                    'helpText': 'Name of the application which contains the wizard, by default the application in which your document is included'
                },
    'domain':   {
                    'question' : 'Domain : ',
                    'key': 'domain',
                    'type': 'string',
                    'helpText': 'Name of the domain in the application, by default the domain is the space'
                },
    'extra':    {
                    'question' : 'Extra : ',
                    'key': 'extra',
                    'type': 'string',
                    'helpText': 'The \'extra\' params used in the wizards'
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
