
var render = function(options) {
    var TEMPLATE_NAME = 'plugin.grid.local',
        body = $.parseJSON(options.body);

    var colNames = [],
        colModel = [];

    $.template(TEMPLATE_NAME,
        "<div><table id='sqlgrid' class='scroll' cellpadding='0' cellspacing='0'></table>" +
        "<div id='gridpager' class='scroll' style='text-align: center;'></div></div>");
    $.tmpl(TEMPLATE_NAME, {}).appendTo(this);

    function createGrid() {
        colNames = body.columns;
        setColModel();

        var grid = $("#sqlgrid", options.pagecontent);
        grid.jqGrid({
            datatype: "json",
            colNames: colNames,
            colModel: colModel,
            pager: (body.page ? "#gridpager" : ""),
            rowNum: body.pagesize,
            sortname: body.sort,
            sortorder: "asc",
            viewrecords: false,
            caption: body.name || "Grid",
            width: body.width || 600,
            autowidth: body.autowidth,
            height: body.height || 400
        });

        grid.addRowData(0, body.data);
    }

    function getKeys(obj) {
        var keys = [],
            propertyName;
        for (propertyName in obj) {
            if (obj.hasOwnProperty(propertyName)) {
                keys.push(propertyName);
            }
        }
        return keys;
    }

    function setColModel() {
        var width = 80,
            i;
        for (i = 0; i < colNames.length; ++i) {
            colname = colNames[i];
            colModel.push({name: colname, index: colname, width: width, align: "left"});
        }
    }

    options.addCss({'id': 'sqlgrid1', 'tag': 'link', 'params':
        {'rel': 'stylesheet', 'href': '/static/lfw/js/libs/jquery.jqGrid-4.0.0/src/css/ui.jqgrid.css'}});
    options.addCss({'id': 'sqlgrid2', 'tag': 'link', 'params':
        {'rel': 'stylesheet', 'href': '/static/lfw/js/libs/jquery.jqGrid-4.0.0/src/css/ui.multiselect.css'}});
    options.addDependency(createGrid, ["/static/lfw/js/libs/jquery.jqGrid-4.0.0/src/i18n/grid.locale-en.js",
        "/static/lfw/js/libs/jquery.jqGrid-4.0.0/js/jquery.jqGrid.min.js",
        "/static/lfw/js/libs/jquery.jqGrid-4.0.0/src/jqModal.js",
        "/static/lfw/js/libs/jquery.jqGrid-4.0.0/src/jqDnR.js"]);
};

register(render);
