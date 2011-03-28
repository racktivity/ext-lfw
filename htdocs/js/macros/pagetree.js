var render = function(options) {

    var TEMPLATE_NAME = 'plugin.page.treeview';
    var $this = $(this);    
    var space = options.space;
    var page = options.page;

    options.addCss({'id': 'pagetree', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': '/js/libs/jquery.treeview/jquery.treeview.css'}});
    options.addCss({'id': 'pagetree_', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': '/js/libs/jquery.treeview/demo/screen.css'}});


    var processData = function(data){
	    children = new Object();
	    dataitems = new Object();
	    childrenitems = new Array();
	    
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
	    
	    $.each(data, function(index, datadict){
	    	var isroot = inArray(datadict.guid, childrenitems);
	    	if (isroot == false) {
	    		href = '/#/' + options.space + '/' + datadict.name;
	    		contents += '<li class="closed"><span><a href="' + href + '">' + datadict.name + '</a></span>';
	    	}
	    	
	    	contents += formRecursiveTree(dataitems, datadict.guid, children);
	    	if (isroot == false){
	    		contents += '</li>';
	    	}
	    })
	    contents += '</ul>';
	    //$('#main').append(contents);
	    
	    var unique = "pagetree_test";
	    $.template(TEMPLATE_NAME, '<div id="${unique}"></div>');
	    $.tmpl(TEMPLATE_NAME, {'unique': unique}).appendTo($this);
	    $('#pagetree_test').append(contents);
    };

    var formRecursiveTree = function(data, elementguid, children){
    	var contents = "";
    	if (elementguid in children) {
    		contents += '<ul>';
    		$.each(children[elementguid], function(index, child) {
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
	    $.get(
	        '/appserver/rest/lfw/pageTree',
	        {
	            space: space,
	        },
	        'json'
	    )
	    .success(function (data, textStatus, jqXHR) {
	        processData(data);
	        $('#treeview').treeview();
	        
	        //$.template(TEMPLATE_NAME, '<div></div>');
	    })
	    .error(function (data, textStatus, jqXHR) {
	        console.log('Failed to get page tree: ' + textStatus);
	    });
    	
    }

	options.addDependency(cb, ["/js/libs/jquery.treeview/jquery.treeview.js"]);	
};

register(render); 
