var render = function(options) {
	var $this = $(this);    

	var cb = function() {
	    var TEMPLATE_NAME = 'plugin.actions.wizardactionlist';
        $.template(TEMPLATE_NAME, '<ul>{{each action}}<li><a href="${uri}" title="${description}}" target="${target}" class="ui-button ui-widget ui-state-default ui-corner-all ui-button-text-icon-primary" role="button" aria-disabled="false"><span class="ui-button-icon-primary ui-icon {{if icon}}${icon}{{/if}}"></span><span class="ui-button-text">${name}</span></a></li>{{/each}}</ul>')
        $.tmpl(TEMPLATE_NAME, {}).appendTo($this);
	};
	
    options.addDependency(cb, 
            ['/static/jswizards/js/jswizards_client.js', 
             '/static/jswizards/js/jswizards.js', 
             '/static/jswizards/js/jswizards_oldstyle.js',
             '/static/jswizards/libs/jquery.form.js', 
             '/static/jswizards/libs/jquery.floatbox.1.0.8.js', 
             '/static/jswizards/libs/jquery-datepicker/demo/scripts/jquery.datePicker.js',
             '/static/jswizards/libs/jquery-datepicker/demo/scripts/date.js', 
             '/static/jswizards/libs/jquery.ui.datetimepicker.js',
             '/static/jswizards/libs/jQueryBubblePopup.v2.3.1_2/jquery.bubblepopup.v2.3.1.min.js',
             '/static/jswizards/libs/jquery-tooltip/js/jtip.js']);
	options.addCss({'id': 'wizardactions', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': '/static/jswizards/style/jquery-ui.css'}});
	options.addCss({'id': 'wizardaction', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': '/static/jswizards/libs/jQueryBubblePopup.v2.3.1_2/jquery.bubblepopup.v2.3.1.css'}});
};
register(render);
