//@metadata wizard=sqlgrid
//@metadata description=Show a table with data taken from specific datasource
//@metadata image=img/macros/sqlgrid.png
//@metadata documentationUrl=http://www.pylabs.org/#/alkiradocs/MacroSqlGrid

var render = function(options) {
    var TEMPLATE_NAME = 'plugin.grid.sql';
    var $this = $(this);
    var space = options.space;
    var page = options.page;
    var body = $.parseJSON(options.body);
    var links = body.link || [];
    var caption = body.name || "SQL Grid";
    var sqlselect = "SELECT ";
    var hidden = body.hidden || [];
    if (body.sqlselect){
        sqlselect = body.sqlselect;
    }else{

        var columns = body.columns;
        var whereclouse = body.wheredict;
        $.each(columns, function(key, value){
            if(!value){
                sqlselect += body.table + "." + key+ ", ";
            }else{
                sqlselect += body.table + "." + key+ " as "+ '"' + value + '", ';
            }
        });
        sqlselect = sqlselect.substr(0, sqlselect.length-2);

    if(whereclouse) {
            sqlselect += " FROM "+body.schema+"."+body.table+" WHERE ";

            $.each(whereclouse, function(key, value){
                sqlselect += body.table + "." + key+" = " + "'" + value + "' and ";
            });
            sqlselect = sqlselect.substr(0, sqlselect.length-5);
    }
      else
            sqlselect += " FROM "+body.schema+"."+body.table;

    }

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

    function setColModel(colNames) {

        var width = 80;
        $.each(colNames, function(index, colname) {
            if (getKeys(body).indexOf('fieldwidth') != -1) {
                if (getKeys(body.fieldwidth).indexOf(colname) != -1) {
                    width = body.fieldwidth[colname];
                }
            }
            if(hidden.indexOf(colname) != -1){
                colModel.push({name: colname, index: colname, width: width, hidden:true});
            }
            else if (colname in links) {
                colModel.push({name: colname, index: colname, width: width, edittype: 'select', formatter: linkFormatter});
            }
            else colModel.push({name: colname, index: colname, width: width, align: 'left'});
        })
    }

    function linkFormatter(cellvalue, options, rowObject) {

        var idx = rowObject.indexOf(cellvalue);
        var columname = colNames[idx];
        var urltemplate = links[columname];
        var regex = /\$([\w\s]+)\$/g;
        urltemplate = urltemplate.replace(regex, function(fullmatch, columnname){
            var colIndx= colNames.indexOf(columnname);
            var value = rowObject[colIndx];
            return value;

        });

        return '<a href= ' + urltemplate + '>'+ cellvalue +'</a>';
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
            url: 'appserver/rest/ui/portal/generic',
            postData: { tagstring: "",
                    sqlselect: sqlselect,
                    table: body.table,
                    schema: body.schema,
                    dbconnection: body.dbconnection,
                    macroname: "sqlgrid"
            },
            datatype: 'json',
            colNames: getColNames(),
            colModel: getColModel(),
            pager: '#gridpager',
            rowNum: body.pagesize,
            sortname: body.sort,
            sortorder: body.sortorder || 'asc',
            viewrecords: false,
            caption: caption,
            width: width,
            height: height,
            scrollOffset : 0,
            forceFit: true
          });
          $("#sqlgrid")[0].addJSONData(data);
    }

    function getData() {
        $.ajax({
            url: 'appserver/rest/ui/portal/generic',
            data: { tagstring: "",
                    sqlselect: sqlselect,
                    table: body.table,
                    schema: body.schema,
                    rows: body.pagesize,
                    dbconnection: body.dbconnection,
                    macroname: "sqlgrid"
            },
            dataType: 'json',
            contentType: "application/json; charset=utf-8",
            success: success,
            error: error
        });
    }

    var cb = function() {
        getData();
    }

    options.addCss({'id': 'sqlgrid1', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': 'js/libs/jquery.jqGrid-4.4.0/src/css/ui.jqgrid.css'}});
    options.addCss({'id': 'sqlgrid2', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': 'js/libs/jquery.jqGrid-4.4.0/src/css/ui.multiselect.css'}});
    options.addDependency(cb, ["js/libs/jquery.jqGrid-4.4.0/src/i18n/grid.locale-en.js", 
        "js/libs/jquery.jqGrid-4.4.0/js/jquery.jqGrid.min.js",
        "js/libs/jquery.jqGrid-4.4.0/src/jqModal.js", 
        "js/libs/jquery.jqGrid-4.4.0/src/jqDnR.js"]);
}
register(render);
