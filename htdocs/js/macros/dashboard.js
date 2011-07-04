var LFW_DASHBOARD = {
    opts: {},
    instance: null,
    widgetTypes: [],
    widgetTypesByName: {}
};

// Menu
$(function() {
    // The Menu class
    function Menu(trigger, container) {
        this.trigger = trigger;
        this.container = container;

        this.container.hide();
        this.container.addClass("menu-container");

        this.itemCount = 0;
        this.subMenus = {};

        // Make the click work
        this.trigger.click($.proxy(this._toggle, this));
    }

    // Add an item to a specific container
    Menu.prototype._addItem = function(parent, text, obj, callback, args, prepend) {
        var toAdd = "<div class='item-" + this.itemCount + " menu-item'>" + text + "</div>";
        if (prepend) {
            parent.prepend(toAdd);
        } else {
            parent.append(toAdd);
        }
        if (obj !== undefined && callback !== undefined) {
            var that = this;
            parent.find(".item-" + this.itemCount).click(function() {
                that.hide();
                callback.call(obj, args);
            });
        }
        this.itemCount++;
    };

    // Add an item to the menu
    Menu.prototype.addItem = function(text, obj, callback, args, prepend) {
        this._addItem(this.container, text, obj, callback, args);
    };

    // Hide the menu
    Menu.prototype.hide = function() {
        $(document).unbind("click.LFW_DASHBOARD.Menu");
        this.container.hide();
    };

    // Toggle the menu
    Menu.prototype._toggle = function() {
        this.container.toggle();
        if (this.container.is(":visible")) {
            var that = this;
            $(document).bind("click.LFW_DASHBOARD.Menu", function(e) { that._click(e); });
        }
    };

    // A global click event occurred, check if we need to hide
    Menu.prototype._click = function(e) {
        if (e.target === this.trigger[0]) { //trigger has already a click callback
            return;
        }
        var target = $(e.target);
        if (target.hasClass("menu-item") || target.parent().hasClass("menu-item")) { //menu item clicked
            return;
        }
        this.hide();
    };

    // Add a submenu to the menu
    Menu.prototype.addSubMenu = function(text, prepend) {
        var toAdd = "<div class='item-" + this.itemCount + " menu-item'>" +
            "<span class='arrow'>&#x25C4;</span>" + text + "</div>";
        if (prepend) {
            this.container.prepend(toAdd);
        } else {
            this.container.append(toAdd);
        }
        var item = this.container.find(".item-" + this.itemCount);

        item.append("<div class='menu-sub menu-container menu-sub-" + this.itemCount + "' />");
        var sub = item.find(".menu-sub-" + this.itemCount);
        sub.hide();
        item.hover(function() { sub.toggle(); });

        this.subMenus[text] = sub;
    };

    // Add an item to a submenu
    Menu.prototype.addSubMenuItem = function(subMenu, text, obj, callback, args, prepend) {
        this._addItem(this.subMenus[subMenu], text, obj, callback, args);
    };

    LFW_DASHBOARD.Menu = Menu;
});

// Widget
$(function() {
    // The Widget class
    function Widget(column, object) {
        // Make sure our object is well defined
        if (object.id === undefined) {
            object.id = new Date().getTime();
        }
        if (object.title === undefined) {
            object.title = "New widget";
        }
        if (object.collapsed === undefined) {
            object.collapsed = false;
        }
        if (object.config === undefined) {
            object.config = "{}";
        } else if (typeof(object.config) !== "string") {
            object.config = $.toJSON(object.config);
        }
        if (object.params === undefined) {
            object.params = "{}";
        } else if (typeof(object.params) !== "string") {
            object.params = $.toJSON(object.params);
        }

        this.options = object;
        this.parent = column;
        this.fullId = "widget" + this.options.id;

        // Add the widget
        var data = $.tmpl('plugin.dashboard.widget', object);
        console.log('Widget Rendered: ' + data.html());
        LFW_DASHBOARD.opts.swap(data, column.jq, true);
        this.jq = column.jq.find("#" + this.fullId);
        var that = this;

        // Make the collapse work
        this.jq.find(".portlet-header .ui-icon-minusthick").click($.proxy(this.toggleCollapse, this));
        if (this.options.collapsed) {
            this.toggleCollapse(true);
        }

        // Create the menu & add remove
        this.menu = new LFW_DASHBOARD.Menu(this.jq.find(".portlet-header .icon-menu"), this.jq.find(".portlet-menu"));
        this.menu.addItem("Configure", this, this.showOptions);
        this.menu.addItem("Remove", this, this._confirmRemoval);

        // Make the icons only show when hovering
        this.jq.mouseenter(function() { that.jq.find(".portlet-header .icons").show(); });
        this.jq.mouseleave(function() {
            that.jq.find(".portlet-header .icons").hide();
            that.menu.hide();
        });
    }

    // Toggle the collapse
    Widget.prototype.toggleCollapse = function(dontSave) {
        this.jq.find(".portlet-header .collapse").toggleClass("ui-icon-minusthick").toggleClass("ui-icon-plusthick");
        this.jq.find(".portlet-content").toggle();

        if (dontSave !== true) {
            this.options.collapsed = !this.options.collapsed;
            LFW_DASHBOARD.opts.saveConfig();
        }
    };

    // Show a dialog to confirm the removal of the widget
    Widget.prototype._confirmRemoval = function() {
        this.jq.append("<div id='dialog-confirm' title='Remove widget'>" +
            "<p><span class='ui-icon ui-icon-alert' style='float:left; margin:0 7px 20px 0;' />" +
                "You will delete \"" + this.options.title + "\".<br />Are you sure?</p></div>");

        var that = this;

        // Ask before removing
        this.jq.find("#dialog-confirm").dialog({
            resizable: false,
            height: "auto",
            modal: true,
            buttons: {
                "Cancel": function() { $(this).dialog("close"); },
                "Delete": function() {
                    that.parent.removeWidget(that);
                    $(this).dialog("close");
                }
            },
            close: function() { $(this).remove(); }
        });
    };

    // Show the options
    Widget.prototype.showOptions = function() {
        var that = this,
            wizard = (LFW_DASHBOARD.widgetTypesByName[this.options.widgettype].wizard ?
                LFW_DASHBOARD.widgetTypesByName[this.options.widgettype].wizard : "general");

        function update(object) {
            object = $.parseJSON(object);
            that.options.title = object.title;
            that.options.config = object.body;
            that.options.params = $.toJSON(object.params);

            that.jq.find(".portlet-header .title").text(that.options.title);
            var data = $.tmpl('plugin.dashboard.widgetcontent', that.options);
            LFW_DASHBOARD.opts.swap(data, that.jq.find(".portlet-content"), false, that.jq.find(".portlet-content"));

            // Make it persistent
            LFW_DASHBOARD.opts.saveConfig();
        }

        var args = { title: this.options.title, body: this.options.config },
            params = $.parseJSON(this.options.params);
        if (!$.isEmptyObject(params)) {
            args.params = params;
        }

        JSWizards.launch("http://" + document.domain + "/" + LFW_CONFIG.appname +
            "/appserver/rest/ui/wizard", "widgets", wizard, $.toJSON(args), update);
    };

    LFW_DASHBOARD.Widget = Widget;
});

// Column
$(function() {
    //Small Column class
    function Column(dashboard, object, width) {
        // Make sure our object is well defined
        if (object.order === undefined) {
            object.order = 0;
        }
        if (!object.widgets) {
            object.widgets = [];
        }

        this.parent = dashboard;
        this.order = parseInt(object.order, 10);
        this.fullId = "column" + this.order;
        this._widgets = object.widgets;
        this.widgets = [];

        // Add the column
        var data = $.tmpl('plugin.dashboard.column', object);
        console.log('Column Rendered: ' + data.html());
        LFW_DASHBOARD.opts.swap(data, dashboard.jq.find(".columns"), true);
        this.jq = dashboard.jq.find(".columns #" + this.fullId);

        // Make the widgets moveable
        this.jq.sortable({
            handle: ".portlet-header",
            forceHelperSize: true,
            tolerance: "pointer",
            connectWith: ".column",
            update: function(event, ui) {
                if (!ui.sender) {
                    that._moveWidget(ui.item[0]);
                }
            }
        });

        // Set width (minus margins and such)
        this.setWidth(width);

        // Sort the widgets by order first
        var that = this;
        this._widgets.sort(function(w1, w2) {
            if (w1.order !== w2.order) {
                return w1.order > w2.order;
            } else {
                return 0;
            }
        });

        // Create the Widgets
        var i;
        for (i = 0; i < this._widgets.length; ++i) {
            this.widgets.push(new LFW_DASHBOARD.Widget(this, this._widgets[i]));
        }
    }

    // Add a widget
    Column.prototype.addWidget = function(id, title, type, order, collapsed, config, params) {
        // Make sure we have an order
        var i;
        if (order === undefined) {
            // Get the maximum order so far and increase it
            order = 0;
            for (i = 0; i < this.widgets.length; ++i) {
                if (this.widgets[i].options.order >= order) {
                    order = this.widgets[i].options.order + 1;
                }
            }
        }

        var object = { id: id, title: title, widgettype: type, order: order, collapsed: collapsed, config: config,
            params: params };
        this.widgets.push(new LFW_DASHBOARD.Widget(this, object));

        // Make it persistant
        this._widgets.push(object);
        LFW_DASHBOARD.opts.saveConfig();
    };

    // Remove a widget
    Column.prototype.removeWidget = function(widget) {
        widget.jq.remove();

        // Make it persistant
        var pos = this.widgets.indexOf(widget);
        if (pos !== -1) {
            this.widgets.splice(pos, 1);
            this._widgets.splice(pos, 1);
        }
        LFW_DASHBOARD.opts.saveConfig();
    };

    // Set the width of the column
    Column.prototype.setWidth = function(width) {
        this.jq.width(width - (this.jq.outerWidth(true) - this.jq.width()) );
    };

    // Move a widget away from the column
    Column.prototype.moveWidgetFrom = function(widgetIndex) {
        var widgetInfo = {};
        widgetInfo.object = this._widgets.splice(widgetIndex, 1)[0];
        widgetInfo.widget = this.widgets.splice(widgetIndex, 1)[0];

        // Resort
        var i;
        for (i = 0; i < this.widgets.length; ++i) {
            this.widgets[i].options.order = i;
        }

        return widgetInfo;
    };

    // Move a widget to the column
    Column.prototype.moveWidgetTo = function(widgetInfo) {
        this._widgets.push(widgetInfo.object);
        this.widgets.push(widgetInfo.widget);

        this.resortFromDOM();
    };

    // Resort the column according to the current DOM
    Column.prototype.resortFromDOM = function() {
        var children = this.jq.children(".portlet");
        var i, j,
            tmpWidgets = $.extend(true, [], this.widgets),
            tmpObjects = $.extend(true, [], this._widgets);

        // Clear the arrays, don't assign new empty arrays!
        this.widgets.length = 0;
        this._widgets.length = 0;

        for (i = 0; i < children.length; ++i) {
            var id = children[i].id;
            var index;

            for (j = 0; j < tmpWidgets.length; ++j) {
                if (tmpWidgets[j].fullId === id) {
                    index = j;

                    tmpWidgets[j].options.order = i;
                    break;
                }
            }

            this.widgets.push(tmpWidgets.splice(index, 1)[0]);
            this._widgets.push(tmpObjects.splice(index, 1)[0]);
        }
    };

    LFW_DASHBOARD.Column = Column;
});

// Dashboard
$(function() {
    // The Dashboard class
    function Dashboard() {
        // Make sure our config is well defined
        if (!LFW_DASHBOARD.opts.config.columns) {
            LFW_DASHBOARD.opts.config.columns = [{}];
        }
        if (!LFW_DASHBOARD.opts.config.id) {
            LFW_DASHBOARD.opts.config.id = "dashboard-id";
        }
        if (!LFW_DASHBOARD.opts.config.title) {
            LFW_DASHBOARD.opts.config.title = "Dashboard";
        }

        this._columns = LFW_DASHBOARD.opts.config.columns;
        this.id = LFW_DASHBOARD.opts.config.id;
        this.columns = [];

        // Add the dashboard
        var data = $.tmpl('plugin.dashboard.main', LFW_DASHBOARD.opts.config);
        console.log('Dashboard Rendered: ' + data.html());
        LFW_DASHBOARD.opts.swap($(data).html());
        this.jq = $("#" + this.id);

        // Disable selection of the headers so we are sure we can always drag them
        this.jq.find(".portlet-header").disableSelection();

        // Configure options
        this.jqOptions = this.jq.find(".dashboard-options");
        this._fillOptions();

        // Make the widget store work
        this.jq.find(".dashboard-header .ui-icon-plusthick").click($.proxy(this.showWidgetStore, this));

        // Make configure work
        var that = this;
        this.jq.find(".dashboard-header .ui-icon-wrench").click(function() { that.jqOptions.dialog("open"); });

        // Sort the columns by order first
        this._columns.sort(function(col1, col2) {
            if (col1.order !== col2.order) {
                return col1.order > col2.order;
            } else {
                return 0;
            }
        });

        // Create the Columns
        var i;
        for (i = 0; i < this._columns.length; ++i) {
            this.columns.push(new LFW_DASHBOARD.Column(this, this._columns[i], this.jq.width() / this._columns.length));
        }
    }

    // Show the widget store
    Dashboard.prototype.showWidgetStore = function() {
        // Create the widget store if needed
        var widgetStore = $("#widgetStore"),
            that = this,
            search;

        if (widgetStore.length === 0) { // Add it
            $("body").append("<div id='widgetStore' title='Widget Store'>" +
                "<div class='column-left'><input type='text' class='search' /><ul class='types'></ul></div>" +
                "<div class='column-right'></div>" +
                "</div>");

            widgetStore = $("#widgetStore");
            widgetStore.dialog({
                autoOpen: false,
                modal: true,
                resizable: false,
                draggable: false,
                minHeight: "auto",
                width: 860,
                buttons: {}
            });

            var display = widgetStore.find(".column-right");

            // Make the quick search work
            search = widgetStore.find(".search");
            search.keyup(function(event) {
                function contains(string, keywords) {
                    var lower = string.toLowerCase(),
                        i;
                    for (i = 0; i < keywords.length; ++i) {
                        if (lower.indexOf(keywords[i]) === -1) {
                            return false;
                        }
                    }
                    return true;
                }

                var types = search.val().split(" "),
                    widgets = [],
                    i, type;

                // Ensure lowercase on the types
                for (i = 0; i < types.length; ++i) {
                    types[i] = types[i].toLowerCase();
                }

                // Search names
                for (i = 0; i < LFW_DASHBOARD.widgetTypes.length; ++i) {
                    type = LFW_DASHBOARD.widgetTypes[i];

                    // Search name
                    if (contains(type.name, types)) {
                        widgets.push(type);
                    }
                }

                // Show results
                display.empty();
                for (i = 0; i < widgets.length; ++i) {
                    type = widgets[i];
                    display.append("<div id='widget-" + type.name + "' class='widgettype'>" +
                        (type.image ? "<img src='" + type.image + "' />" : "<img src='img/pixel.gif' />") +
                        "<button class='add'><span class='ui-button-text'>Pick me</span></button>" +
                        "<h3>" + type.name + "</h3><p>" + (type.description ? type.description : "No description") +
                        "</p></div>");
                }

                // Make em clickable
                display.find(".add").click(function() {
                    type = $(this).parent().attr("id").replace("widget-", "");

                    // Get the column with the least amount of widgets
                    var column = that.columns[0];
                    for (i = 0; i < that.columns.length; ++i) {
                        if (that.columns[i].widgets.length < column.widgets.length) {
                            column = that.columns[i];
                        }
                    }

                    var wizard = (LFW_DASHBOARD.widgetTypesByName[type].wizard ?
                        LFW_DASHBOARD.widgetTypesByName[type].wizard : "general");

                    function add(object) { // Add the widget
                        object = $.parseJSON(object);
                        column.addWidget(undefined, object.title, type, undefined, false, object.body, object.params);
                    }

                    JSWizards.launch("http://" + document.domain + "/" + LFW_CONFIG.appname +
                        "/appserver/rest/ui/wizard", "widgets", wizard, "", add);

                    widgetStore.dialog("close");
                });

                display.find(".widgettype").hover(function() { $(this).toggleClass("ui-state-hover"); });
            });
        }

        // Update types
        search = widgetStore.find(".search");
        var typeContainer = widgetStore.find(".types"),
            type;
        typeContainer.empty();
        typeContainer.append("<li title=''>All (" + LFW_DASHBOARD.widgetTypes.length + ")</li>");
        for (i = 0; i < LFW_DASHBOARD.widgetTypes.length; ++i) {
            type = LFW_DASHBOARD.widgetTypes[i];
            typeContainer.append("<li title='" + type.name +"'>" + type.name + "</li>");
        }
        // Make em clickable
        typeContainer.find("li").click(function(event) {
            search.val(this.title);
            search.keyup();
            event.preventDefault();
        });

        // Show the widget center
        search.val("");
        search.keyup();
        widgetStore.dialog("open");
    };

    // Show the options
    Dashboard.prototype._fillOptions = function() {
        var titleElem = this.jqOptions.find(".options-title"),
            columnElem = this.jqOptions.find(".options-columns"),
            that = this;

        titleElem.val(LFW_DASHBOARD.opts.config.title);
        columnElem.val(this._columns.length);

        function cancel() {
            that.jqOptions.dialog("close");
            titleElem.val(LFW_DASHBOARD.opts.config.title);
            columnElem.val(that._columns.length);
        }

        function ok() {
            that.jqOptions.dialog("close");

            LFW_DASHBOARD.opts.config.title = titleElem.val();

            that.jq.find(".dashboard-header .title").text(LFW_DASHBOARD.opts.config.title);

            var columnCount = parseInt(columnElem.val(), 10);
            var width, i;
            if (columnCount > that._columns.length) { // Add columns
                // Change the width of the current columns
                width = that.jq.width() / columnCount;
                for (i = 0; i < that.columns.length; ++i) {
                    that.columns[i].setWidth(width);
                }

                // Add new columns
                while (that._columns.length !== columnCount) {
                    that._columns.push({ order: that._columns.length, widgets: [] });
                    that.columns.push(new LFW_DASHBOARD.Column(that, that._columns[that._columns.length - 1], width));
                }
            } else if (columnCount < that._columns.length) { // Remove columns
                // Remove columns
                var widgets = [], column;
                while (that._columns.length !== columnCount) {
                    column = that._columns.pop();
                    widgets = widgets.concat(column.widgets);
                    column = that.columns.pop();
                    column.jq.remove();
                }

                // Change the width of the columns that are left over
                width = that.jq.width() / columnCount;
                for (i = 0; i < that.columns.length; ++i) {
                    that.columns[i].setWidth(width);
                }

                // Add all the widgets to the last column
                column = that.columns[that.columns.length - 1];
                for (i = 0; i < widgets.length; ++i) {
                    var widget = widgets[i];
                    column.addWidget(undefined, widget.title, widget.widgettype, undefined, widget.collapsed,
                        widget.config, widget.params);
                }
            }

            // Make it persistent
            LFW_DASHBOARD.opts.saveConfig();
        }

        // Make the dialog work
        this.jqOptions.dialog({
            autoOpen: false,
            modal: true,
            resizable: false,
            draggable: false,
            minHeight: "auto",
            width: "auto",
            buttons: {
                "Cancel": cancel,
                "Ok": ok
            }
        });
    };

    // Move a widget from one column to another
    Dashboard.prototype._moveWidget = function(divWidget) {
        var toColumn, fromColumn, column, i, j, widgetIndex;

        for (i = 0; i < this.columns.length; ++i) {
            column = this.columns[i];
            if (column.fullId === divWidget.parentNode.id) {
                toColumn = this.columns[i];
            }

            for (j = 0; j < column.widgets.length; ++j) {
                if (column.widgets[j].fullId === divWidget.id) {
                    widgetIndex = j;
                    fromColumn = column;
                    break;
                }
            }
        }

        if (!toColumn) {
            return;
        }

        if (toColumn !== fromColumn) { // Move the widget in the structure
            toColumn.moveWidgetTo(fromColumn.moveWidgetFrom(widgetIndex));
        } else {
            toColumn.resortFromDOM();
        }

        // Persist it
        LFW_DASHBOARD.opts.saveConfig();
    };

    LFW_DASHBOARD.Dashboard = Dashboard;
});

var render = function(options) {
    LFW_DASHBOARD.opts = options;

    // CSS
    options.addCss({'id': 'dashboardmacro', 'tag': 'style', 'params': '.dashboard { margin: 0px; }' +
        '.dashboard-options .options-table .options-textnode { vertical-align: middle; }' +
        '.dashboard-header { margin: 0.3em; padding-bottom: 4px; padding-left: 0.2em; }' +
        '.dashboard-header .ui-icon { float: right; cursor: pointer; }' +
        '.dashboard .columns .column { margin: 0px; float: left; padding: 10px; }' +
        '.portlet { margin: 0 0 1em 0; position: relative; }' +
        '.portlet-header { margin: 0.3em; padding-bottom: 4px; padding-left: 0.2em; cursor: move; }' +
        '.portlet-header .icons { float: right; display: none; }' +
        '.portlet-header .icons .ui-icon { float: right; cursor: pointer; }' +
        '.portlet .portlet-menu { position: absolute; z-index: 1000; right: 5px; top: 20px; }' +
        '.portlet .portlet-content { padding: 0.4em; }' +
        '.ui-sortable-placeholder { border: 1px dotted black; visibility: visible !important; height: 50px' +
            '!important; }' +
        '.ui-sortable-placeholder * { visibility: hidden; }' +
        '#widgetStore { font-size: 1.1em; }' +
        '#widgetStore .column-left { width: 22%; float: left; height: 414px; border-right: 1px solid #999;' +
            ' margin-left: -1px; overflow: auto; }' +
        '#widgetStore .column-left .search { width: 90%; font-size: 100%; }' +
        '#widgetStore .column-left li { margin-top: 5px; cursor: pointer; }' +
        '#widgetStore .column-right { width: 78%; float: left; overflow: auto; height: 414px; }' +
        '#widgetStore .column-right .widgettype { padding: 0 20px 0 140px; width: 150px; height: 140px; float: left;' +
            ' overflow: hidden; border: 0px; }' +
        '#widgetStore .column-right .widgettype button { margin: 81px 0 0 -131px; float: left; }' +
        '#widgetStore .column-right .widgettype img { margin: 10px 0 0 -130px; border: 1px solid #999; float: left; ' +
            'width: 120px; height: 60px; }' +
        '#widgetStore .column-right .widgettype h3 { margin: 11px 0px 5px 0px; font-size: 1em; }' +
        '#widgetStore .column-right .widgettype p { height: 100px; overflow: hidden; }' +
        '.menu-container { border: 1px solid #888888; background: #FFFFFF; }' +
        '.menu-item { padding: 5px 15px 5px 15px; cursor: pointer; background: #FFFFFF; position: relative; }' +
        '.menu-item:hover { background-color: #EEEEEE; }' +
        '.menu-item .arrow { position: absolute; left: 0px; }' +
        '.menu-sub { position: absolute; right: 100%; top: -1px; }'
    });

    // Get dashboard
    if ($.isEmptyObject(LFW_DASHBOARD.opts.config)) { // Get the default from the body
        try {
            LFW_DASHBOARD.opts.config = $.parseJSON(options.body);
        } catch (e) {}
    }

    // Define templates
    // @todo: Check if templates are already compiled
    $.template('plugin.dashboard.main',
        '<div class="bogus">' +
            '<div class="dashboard ui-widget ui-widget-content ui-helper-clearfix ui-corner-all" id="${id}">' +
                '<div class="dashboard-options" title="Dashboard options">' +
                    '<table class="options-table">' +
                        '<tr><td class="options-textnode">Title:</td>' +
                        '<td align="left"><input type="text" class="options-title" value="" /></td></tr>' +
                        '<tr><td class="options-textnode">Number of columns:</td>' +
                        '<td align="left"><select class="options-columns"><option value="1">1</option>' +
                            '<option value="2">2</option><option value="3">3</option></select></td></tr>' +
                    '</table></div>' +
                '<div class="dashboard-header ui-widget-header ui-corner-all">' +
                    '<span class="ui-icon ui-icon-plusthick" /><span class="ui-icon ui-icon-wrench" />' +
                        '<pan class="title">${title}</span></div>' +
                '<div class="columns"></div>' +
            '</div>' +
        '</div>');
    $.template('plugin.dashboard.column', '<div id="column${order}" class="column"></div>');
    $.template('plugin.dashboard.widget',
        '<div id="widget${id}" class="portlet ui-widget ui-widget-content ui-helper-clearfix ui-corner-all">' +
            '<div class="portlet-header ui-widget-header ui-corner-all">' +
                '<span class="icons"><span class="ui-icon ui-icon-triangle-1-s icon-menu" />' +
                '<span class="ui-icon ui-icon-minusthick collapse" /></span><span class="title">${title}</span></div>' +
            '<div class="portlet-menu" />' +
            '<div class="portlet-content">' +
                '{{tmpl "plugin.dashboard.widgetcontent"}}' +
            '</div>' +
        '</div>');
    $.template('plugin.dashboard.widgetcontent',
        '<div class="macro macro_${widgettype}" {{if params}}params="${params}"{{/if}}>${config}</div>');


    function create() {
        // Load the data first
        $.get("appserver/rest/ui/portal/generic", { tagstring: "", macroname: "macrolist" }, function(data) {
            LFW_DASHBOARD.widgetTypes = data;

            // Exclude the dashboard macro itself and create widgetTypesByName
            var i, indexToRemove = -1;
            for (i = 0; i < data.length; ++i) {
                if (data[i].name !== "dashboard") {
                    LFW_DASHBOARD.widgetTypesByName[data[i].name] = data[i];
                } else {
                    indexToRemove = i;
                }
            }
            if (indexToRemove !== -1) {
                LFW_DASHBOARD.widgetTypes.splice(indexToRemove, 1);
            }

            // Create the dashboard
            LFW_DASHBOARD.instance = new LFW_DASHBOARD.Dashboard();
        });
    }

    options.addDependency(create, ['/static/jswizards/ext/jquery-ui.min.js', '/static/jswizards/js/jswizards.js',
        '/static/jswizards/ext/jquery.floatbox.1.0.8.js', '/static/jswizards/ext/jquery.ui.datetimepicker.js']);
    options.addCss({'id': 'jquery-ui', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href':
        '/static/jswizards/ext/jquery-ui.css'}});
    options.addCss({'id': 'floatbox-wizard', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href':
        '/static/jswizards/ext/joshuaclayton-blueprint-css-c20e981/blueprint/screen.css'}});
    // When enabled this one ruins the whole thing
    /*options.addCss({'id': 'floatbox-wizard-btn', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href':
        '/static/jswizards/ext/joshuaclayton-blueprint-css-c20e981/blueprint/plugins/buttons/screen.css'}});*/
    options.addCss({'id': 'wizardaction', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href':
        '/static/jswizards/style/screen.css'}});
};

register(render);
