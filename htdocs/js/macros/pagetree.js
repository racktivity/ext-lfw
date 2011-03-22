var render = function(options) {

    var TEMPLATE_NAME = 'plugin.page.treeview';
    var $this = $(this);    
    var space = options.space;
    var page = options.page;
    
    $.get(
        '/appserver/rest/lfw/pageTree',
        {
            space: space,
        },
        'json'
    )
    .success(function (data, textStatus, jqXHR) {
        processData(data);
        
        $.template(TEMPLATE_NAME, '<div></div>');
        $.tmpl(TEMPLATE_NAME, {}).appendTo($this);
    })
    .error(function (data, textStatus, jqXHR) {
        console.log('Failed to get page tree: ' + textStatus);
    });
    
    var processData = function(data){
	    children = new Object();
	    dataitems = new Object();
	    childrenitems = new Array();
	    
	    $('body').append('<iframe id="pagetreeframe" scrolling="auto" width="100%" height="100%" align="right"></iframe>');
	    
	    contents = '';
		contents += '<ul id="treeview">';
	    $.each(data, function(index, datadict) {
	    	if (datadict["parent"] != null){
	    		if (children[datadict['parent']] == undefined){
	    			children[datadict['parent']] = new Array();
	    		}
	    		children[datadict['parent']].push(datadict['guid']);
	    		childrenitems.push(datadict['guid']);
	    	}
	    	dataitems[datadict['guid']] = datadict;
	    })
	    
	    console.log(children);
	    console.log(dataitems);
	    console.log(childrenitems);
	    
	    $.each(data, function(index, datadict){
	    	var isroot = inArray(datadict.guid, childrenitems);
	    	if (isroot == false) {
	    		console.log('Adding parent page ' + datadict.name);
	    		href = '/#/' + options.space + '/' + datadict.name;
	    		contents += '<li class="closed"><span><a href="' + href + '">' + datadict.name + '</a></span>';
	    	}
	    	
	    	contents += formRecursiveTree(dataitems, datadict.guid, children);
	    	if (isroot == false){
	    		contents += '</li>';
	    	}
	    })
	    contents += '</ul>';
	    $('#main').append(contents);
    };

    var formRecursiveTree = function(data, elementguid, children){
    	var contents = "";
    	if (elementguid in children) {
    		console.log('in formrecursivetree element ' + data[elementguid].name);
    		contents += '<ul>';
    		$.each(children[elementguid], function(index, child) {
    			console.log('adding child ' + data[child].name);
    			href = '/#/' + options.space + '/' + data[child].name;
    			contents += '<li class="closed"><span><a href="' + href + '">' + data[child].name + '</a></span>';
    			contents += formRecursiveTree(data, child, children);
    			contents += '</li>';
    		})
    		contents += '</ul>';
    		return contents;
    	}
    	else return '';
    }
    
	function inArray(element, array) {
		for (index in array) {
			if (array[index] == element) {
				return true;
			}
		}
		return false;
	}

    var cb = function(){
    	$('#treeview').treeview();
    }

    options.addCss({'id': 'pagetree', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': 'http://jquery.bassistance.de/treeview/jquery.treeview.css'}});
    options.addCss({'id': 'pagetree_', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': 'http://jquery.bassistance.de/treeview/demo/screen.css'}});
    options.addDependency(cb, ["http://jquery.bassistance.de/treeview/jquery.treeview.js"]);
};

register(render); 
