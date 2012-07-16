//@metadata description=Show a table with local data taken from the body of the macro
//@metadata image=img/macros/grid.png
//@metadata documentationUrl=http://www.pylabs.org/#/alkiradocs/MacroGrid

var render = function(options) {
    var TEMPLATE_NAME = 'plugin.grid.local',
        body = $.parseJSON(options.body),
        colNames = [],
        colModel = [],
        dataModel = [],
        now = (new Date()).getTime(),
        gridId = "grid-" + now,
        gridpagerId = "gridpager-" + now;

    $.template(TEMPLATE_NAME,
        "<div><table id='" + gridId + "' class='scroll' cellpadding='0' cellspacing='0'></table>" +
        (body.page ? "<div id='" + gridpagerId + "' class='scroll' style='text-align: center;' />" : "") +
        "</div>");
    $.tmpl(TEMPLATE_NAME, {}).appendTo(this);

    function createGrid() {
        colNames = body.columns;
        dataModel = body.model || [];
        setColModel();

        var grid = $("#" + gridId, options.pagecontent);
        grid.jqGrid({
            datatype: "json",
            colNames: colNames,
            colModel: colModel,
            pager: (body.page ? gridPagerId : ""),
            rowNum: body.pagesize,
            sortname: body.sort,
            sortorder: "asc",
            viewrecords: false,
            caption: (body.hidetitlebar ? "" : body.name || "Grid"),
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
            var colname = colNames[i];
            var model = dataModel[i] || {};
            colModel.push({name: colname, index: colname, width: model['width'] || width, align: model['align'] || "left",
                           sortable:typeof(model.sortable)==='undefined' ? true : model.sortable});
        }
    }

    options.addCss({'id': 'sqlgrid1', 'tag': 'link', 'params':
        {'rel': 'stylesheet', 'href': 'js/libs/jquery.jqGrid-4.4.0/src/css/ui.jqgrid.css'}});
    options.addCss({'id': 'sqlgrid2', 'tag': 'link', 'params':
        {'rel': 'stylesheet', 'href': 'js/libs/jquery.jqGrid-4.4.0/src/css/ui.multiselect.css'}});
    options.addDependency(createGrid, ["js/libs/jquery.jqGrid-4.4.0/src/i18n/grid.locale-en.js",
        "js/libs/jquery.jqGrid-4.4.0/js/jquery.jqGrid.min.js",
        "js/libs/jquery.jqGrid-4.4.0/src/jqModal.js",
        "js/libs/jquery.jqGrid-4.4.0/src/jqDnR.js"], true);
};

register(render);
