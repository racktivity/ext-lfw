var render = function(options) {
	var $this = $(this);    

	var cb = function() {
	    var TEMPLATE_NAME = 'plugin.actions.wizardactionlist';
        $.template(TEMPLATE_NAME, '<ul>{{each action}}<li><a href="${uri}" title="${description}}" target="${target}" class="ui-button ui-widget ui-state-default ui-corner-all ui-button-text-icon-primary" role="button" aria-disabled="false"><span class="ui-button-icon-primary ui-icon {{if icon}}${icon}{{/if}}"></span><span class="ui-button-text">${name}</span></a></li>{{/each}}</ul>')
        $.tmpl(TEMPLATE_NAME, {}).appendTo($this);
        
     //   $('#wizardsform').append("<li><a href='javascript:start('bla','hellowizard','172.19.6.163',success)' target='#'>Hello wizard</a></li>");
        
/**
<form method="post" action="#/action/hellowizard">
    <li><a href="javascript:start('bla','hellowizard','172.19.6.163',success)" target='#'>Hello wizard</a></li>
    <li><a href="javascript:start('bla','hellowizardname','172.19.6.163',success)" target='#'>Hello wizard with name</a></li>
</form>
**/

	};
	
	options.addDependency(cb, ['/js/js/jswizards_client.js', 'js/js/jswizards.js', '/js/js/jswizards_oldstyle.js', \
	'https://github.com/malsup/form/raw/master/jquery.form.js?v2.43', '/js/libs/jquery.floatbox.1.0.8.js', \
	'/js/libs/jquery-datepicker/demo/scripts/jquery.datePicker.js', '/js/libs/jquery-datepicker/demo/scripts/jquery.datePicker.js', \
	'/js/libs/jquery-datepicker/demo/scripts/date.js', '/js/libs/jquery.ui.datetimepicker.js'])
	
	options.addCss({'id': 'wizardactions', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': 'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/themes/base/jquery-ui.css'}})
};
register(render);
