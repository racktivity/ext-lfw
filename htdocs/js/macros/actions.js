var render = function(options) {

    var TEMPLATE_NAME = 'plugin.actions.actionlist';
    var $this = $(this);    
    var space = options.space;
    var page = options.page;
    var widget_type = 'action';
    var widget = 'widget2';
    
    var view = {"action": [
        {"name": "Print", "description": "Print this page", "uri": "javascript:print();", "target": "", "icon": "ui-icon-print"},
        {"name": "Google", "description": "Go To Google", "uri": "http://www.google.com", "target": "_blank", "icon": "ui-icon-link"},        
    ]};
        
    $.get(
        '/appserver/rest/widget_service/getWidgetConfig',
        {
            space: space,
            pagename: page,
            widget_id: widget,
            widget_type: widget_type,
            parentwidget_id: ''
        },
        'json'
    )
    .success(function (data, textStatus, jqXHR) {
        console.log('Got config: ' + $.toJSON(data));
        
        $.template(TEMPLATE_NAME, '<ul>{{each action}}<li><a href="${uri}" title="${description}}" target="${target}" class="ui-button ui-widget ui-state-default ui-corner-all ui-button-text-icon-primary" role="button" aria-disabled="false"><span class="ui-button-icon-primary ui-icon {{if icon}}${icon}{{/if}}"></span><span class="ui-button-text">${name}</span></a></li>{{/each}}</ul>')
        $.tmpl(TEMPLATE_NAME, data).appendTo($this);
    })
    .error(function (data, textStatus, jqXHR) {
        console.log('Failed to get config: ' + textStatus);
    });

    // @todo: Check if template is already compiled
    //$.template(TEMPLATE_NAME, '<ul>{{each action}}<li><a href="${uri}" title="${description}}" target="${target}" class="ui-button ui-widget ui-state-default ui-corner-all ui-button-text-icon-primary" role="button" aria-disabled="false"><span class="ui-button-icon-primary ui-icon {{if icon}}${icon}{{/if}}"></span><span class="ui-button-text">${name}</span></a></li>{{/each}}</ul>')
    //$.tmpl(TEMPLATE_NAME, config).appendTo(this);
}

register(render);
