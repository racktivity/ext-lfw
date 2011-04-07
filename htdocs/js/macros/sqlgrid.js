var render = function(options) {
    var TEMPLATE_NAME = 'plugin.grid.sql';
    var $this = $(this);    
    var space = options.space;
    var page = options.page;
    var body = JSON.parse(options.body);
    var links = body.link;
    console.log(body);
  
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
			links = links.split(",");
			}
		var width = 80;
		$.each(colNames, function(index, colname) {
			if (inArray('fieldwidth', getKeys(body))) {
				if (inArray(colname, getKeys(body.fieldwidth))) {
					width = body.fieldwidth[colname];
				}
			}
			if (inArray(colname, links)) {
				colModel.push({name: colname, index: colname, width: width, edittype: 'select', formatter: linkFormatter});
			}
			else colModel.push({name: colname, index: colname, width: width, align: 'left'});
		})
    }
    
    function linkFormatter(cellvalue, options, rowObject) {
    	return '<a href= /#/' + space + '/' + cellvalue + '>' + cellvalue + '</a>';
    }
    
    function getColModel() {
    	return colModel;
    }
    
    function error(data) {
    	console.log(data);
    }
    
    function makeGrid(data){
    	var height = body.height || 400;
    	var width = body.width || 600;
    	console.log(data);
    	jQuery('#sqlgrid').jqGrid({
    		url: '/appserver/rest/lfw/query?fields=' + body.fields + '&table=' + body.table + '&schema=' + body.schema + '&dbconnection=' + body.dbconnection,
			datatype: 'json',
			colNames: getColNames(),
          	colModel: getColModel(),
            pager: '#gridpager',
            rowNum: body.pagesize,
            sortname: body.sort,
            sortorder: 'asc',
            viewrecords: false,
            caption: 'SQL Grid',
            width: width,
            height: height
          });
          $("#sqlgrid")[0].addJSONData(data);
    }

    function getData() {
    	$.ajax({
    		url: '/appserver/rest/lfw/query?fields=' + body.fields + '&table=' + body.table + '&schema=' + body.schema + '&rows=' + body.pagesize + '&dbconnection=' + body.dbconnection,
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
    
    options.addCss({'id': 'sqlgrid1', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': '/static/lfw/js/libs/jquery.jqGrid-3.8.2/src/css/ui.jqgrid.css'}});
    options.addCss({'id': 'sqlgrid2', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': '/static/lfw/js/libs/jquery.jqGrid-3.8.2/src/css/ui.multiselect.css'}});
    options.addDependency(cb, ["/static/lfw/js/libs/jquery.jqGrid-3.8.2/src/i18n/grid.locale-en.js", "/static/lfw/js/libs/jquery.jqGrid-3.8.2/js/jquery.jqGrid.min.js","/static/lfw/js/libs/jquery.jqGrid-3.8.2/src/jqModal.js", "/static/lfw/js/libs/jquery.jqGrid-3.8.2/src/jqDnR.js"]);
}
register(render);

