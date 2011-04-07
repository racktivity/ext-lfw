var render = function(options) {

    var TEMPLATE_NAME = 'plugin.page.treeview';
    var $this = $(this);    
    var space = options.space;
    var page = options.page;
    
    $.template(TEMPLATE_NAME, '<div><div id="mytree"></div></div>');
    $.tmpl(TEMPLATE_NAME, {}).appendTo($this);

	options.addCss({'id': 'jsicon', 'tag': 'link', 'params': {'rel': 'shortcut icon', 'href': '/favicon.ico'}});
	options.addCss({'id': 'jstree', 'tag': 'link', 'params': {'rel': 'alternate', 'type': 'application/rss+xml', 'href': 'http://www.jstree.com/feed'}});
	options.addCss({'id': 'pagetree', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': 'http://static.jstree.com/v.1.0rc2/_docs/!style.css'}});
	options.addCss({'id': 'canonical', 'tag': 'link', 'params': {'rel': 'canonical', 'href': 'http://www.jstree.com/demo'}});

    var cb = function(){
    	
    	$('#mytree').jstree({
    		"json_data": {
    			"ajax": {
    				"url": "appserver/rest/ui/portal/pageTree?space=" + space,
    				"data": function(n) {
    					return {id: n.attr ? n.attr("id") : 0};
    				},
    			"progressive_render" : true
    			}
    		},
    		"plugins": ["themes", "json_data"]
    	});
    	
    }

	options.addDependency(cb, ["http://static.jstree.com/v.1.0rc2/jquery.cookie.js", "http://static.jstree.com/v.1.0rc2/jquery.hotkeys.js", "http://static.jstree.com/v.1.0rc2/jquery.jstree.js"]);	
};

register(render); 
