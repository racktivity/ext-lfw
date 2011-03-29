var render = function(options) {
    var TEMPLATE_NAME = 'plugin.grid.sql';
    var $this = $(this);    
    var space = options.space;
    var page = options.page;
    var body = JSON.parse(options.body);
    var links = body.link;
  
    console.log('**********', JSON.parse(options.body));
    var colNames = new Array();
    var colModel = new Array();

    $.template(TEMPLATE_NAME, '<div><table id="sqlgrid" class="scroll" cellpadding="0" cellspacing="0"></table><div id="gridpager" class="scroll" style="text-align: center;"></div></div>');
    $.tmpl(TEMPLATE_NAME, {}).appendTo($this);
    
    function success(jsondata) {
    	setColNames(jsondata);
    	setColModel(getColNames());
    	makeGrid(jsondata);
   };
    
    function getKeys(obj) {
    	var keys = [];
    	for (var propertyName in obj) {
    		keys.push(propertyName);
    	}
    	return keys;
    }
    
    function setColNames(data) {
    	colNames = data['columns'];
    }
    
    function getColNames() {
    	return colNames;
    }
    
	function inArray(element, array) {
		for (index in array) {
			if (array[index] == element) {
				return true;
			}
		}
		return false;
	}

    function setColModel(colNames) {
    	if (links != undefined && links != "") {
			console.log('Links: ');
			console.log(links);
			links = links.split(",");
			}
		$.each(colNames, function(index, colname) {
			colModel.push({name: colname, index: colname, width: 80, align: 'left'});
		})
    }
    
    function getColModel() {
    	return colModel;
    }
    
    function error(data) {
    	console.log(data);
    }
    
    function makeGrid(data){
    	console.log('In make grid');
    	console.log(data);
    	jQuery('#sqlgrid').jqGrid({
    		url: '/appserver/rest/lfw/query?sql=' + body.sql + '&dbname=' + body.dbname,
			datatype: 'json',
			colNames: getColNames(),
          	colModel: getColModel(),
            pager: '#gridpager',
            rowNum: body.pagesize,
            sortname: body.sort,
            sortorder: 'desc',
            viewrecords: false,
            caption: 'sql Grid',
            width: 600
          });
          $("#sqlgrid")[0].addJSONData(data);
    }

    function getData() {
    	console.log('In getData');
    	$.ajax({
    		url: '/appserver/rest/lfw/query?sql=' + body.sql + '&rows=' + body.pagesize + '&dbname=' + body.dbname,
    		data: "{}",
    		dataType: 'json',
    		type: 'POST',
    		contentType: "application/json; charset=utf-8",
    		success: success,
    		error: error
    	});
    }
    
    var cb = function() {
    	getData();
    }
    
    options.addCss({'id': 'sqlgrid1', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': '/js/libs/jquery.jqGrid-3.8.2/src/css/ui.jqgrid.css'}});
    options.addCss({'id': 'sqlgrid2', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': '/js/libs/jquery.jqGrid-3.8.2/src/css/ui.multiselect.css'}});
    options.addDependency(cb, ["/js/libs/jquery.jqGrid-3.8.2/src/i18n/grid.locale-en.js", "/js/libs/jquery.jqGrid-3.8.2/js/jquery.jqGrid.min.js","/js/libs/jquery.jqGrid-3.8.2/src/jqModal.js", "/js/libs/jquery.jqGrid-3.8.2/src/jqDnR.js"]);
}
register(render);
