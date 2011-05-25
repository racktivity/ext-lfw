var render = function(options) {

    var TEMPLATE_NAME = 'plugin.actions.actionlist';
    var $this = $(this); 
    
    tagstring = $.trim(options.body);   
    tagstring = tagstring + ' page:' + options.page;
    tagstring = tagstring + ' space:' + options.space;
    macroname = 'actions'
    
    $.get(
        'appserver/rest/ui/portal/generic',
        {
        tagstring: tagstring,
        macroname: macroname
        },
        'json'
    )
    .success(function (data, textStatus, jqXHR) {
        console.log('Got config: ' + $.toJSON(data));
        
        $.template(TEMPLATE_NAME, '{{each action}}<a href="${uri}" title="${description}" target="${target}" class="ui-button ui-widget ui-state-default ui-corner-all ui-button-text-icon-primary" role="button" aria-disabled="false"><span class="ui-button-icon-primary ui-icon {{if icon}}${icon}{{/if}}"></span><span class="ui-button-text">${name}</span></a><br /><br />{{/each}}')
        $.tmpl(TEMPLATE_NAME, data).appendTo($this);
    })
    .error(function (data, textStatus, jqXHR) {
        console.log('Failed to get config: ' + textStatus);
    });
};
register(render);
