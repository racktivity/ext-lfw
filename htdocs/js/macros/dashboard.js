var LFW_DASHBOARD = {
    opts: {},
    instance: null
};

///TODO content with new lines gives problems
///TODO configure dashboard (# of columns)
///TODO persist dragging
///TODO stop dragging when you select everywhere, just let the header drag

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
            object.id = Math.random();
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

        // Add the widget
        var data = $.tmpl('plugin.dashboard.widget', object);
        console.log('Widget Rendered: ' + data.html());
        LFW_DASHBOARD.opts.swap(data, column.jq, true);
        this.jq = column.jq.find("#widget" + this.options.id);
        var that = this;

        // Hide the options
        this.jqOptions = this.jq.find(".portlet-options");
        this._toggleOptions();

        // Make the collapse work
        this.jq.find(".portlet-header .ui-icon-minusthick").click($.proxy(this._toggleCollapse, this));
        if (this.options.collapsed) {
            this._toggleCollapse(true);
        }

        // Create the menu & add remove
        this.menu = new LFW_DASHBOARD.Menu(this.jq.find(".portlet-header .icon-menu"), this.jq.find(".portlet-menu"));
        this.menu.addItem("Configure", this, this._toggleOptions);
        this.menu.addItem("Remove", this, this._confirmRemoval);

        // Make the icons only show when hovering
        this.jq.mouseenter(function() { that.jq.find(".portlet-header .icons").show(); });
        this.jq.mouseleave(function() {
            that.jq.find(".portlet-header .icons").hide();
            that.menu.hide();
        });

        this._fillOptions();
    }

    // Toggle the collapse
    Widget.prototype._toggleCollapse = function(dontSave) {
        if (this.jqOptions.is(":visible")) { // Disable when we are showing the options
            return;
        }

        this.jq.find(".portlet-header .collapse").toggleClass("ui-icon-minusthick").toggleClass("ui-icon-plusthick");
        this.jq.find(".portlet-content").toggle();

        if (!dontSave) {
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

    // Toggle the options
    Widget.prototype._toggleOptions = function() {
        if (this.jqOptions.is(":visible")) {
            this.jqOptions.hide();
            this.jq.find(".portlet-content").show();
        } else {
            this.jq.find(".portlet-content").hide();
            this.jqOptions.show();
        }
    };

    // Fill the options and make them work
    Widget.prototype._fillOptions = function() {
        // Don't do it inline because if the string contains ' then we're fucked
        var titleElem = this.jqOptions.find(".options-title"),
            contentElem = this.jqOptions.find(".options-content"),
            that = this,
            isOk = false,
            ignoreSubmit = false;

        titleElem.val(this.options.title);
        contentElem.val(this.options.config);

        function cancel() {
            ignoreSubmit = true;
            titleElem.val(that.options.title);
            contentElem.val(that.options.config);
        }

        function ok() {
            isOk = true;
            ignoreSubmit = true;
            that._toggleOptions();

            that.options.title = titleElem.val();
            that.options.config = contentElem.val();

            that.jq.find(".portlet-header .title").text(that.options.title);
            LFW_DASHBOARD.opts.swap(that.options.config, that.jq.find(".portlet-content .macro"));

            // Make it persistent
            LFW_DASHBOARD.opts.saveConfig();
            isOk = false;
        }

        // Cancel button
        this.jqOptions.find(".options-cancel").click(function() {
            that._toggleOptions();
            cancel();
        });
        // Ok button
        this.jqOptions.find(".options-ok").click(ok);
        this.jqOptions.find("form").submit(function() {
            if (!ignoreSubmit) {
                ok();
                ignoreSubmit = false;
            }
            return false;
        });
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
        this._widgets = object.widgets;
        this.widgets = [];

        // Add the column
        var data = $.tmpl('plugin.dashboard.column', object);
        console.log('Column Rendered: ' + data.html());
        LFW_DASHBOARD.opts.swap(data, dashboard.jq.find(".columns"), true);
        this.jq = dashboard.jq.find(".columns #column" + this.order);

        // Set width (minus margins and such)
        this.jq.width(width - (this.jq.outerWidth(true) - this.jq.width()) );

        // Sort the widgets by order first
        var that = this;
        this._widgets.sort(function(w1, w2) {
            if (w1.order !== w2.order) {
                return w1.order < w2.order;
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
    Column.prototype.addWidget = function(id, title, type, order) {
        // Make sure we have an order
        var i;
        if (order === undefined) {
            // Get the maximum order so far and increase it
            order = 0;
            for (i = 0; i < this.widgets.length; ++i) {
                if (this.widgets[i].order >= order) {
                    order = this.widgets[i].order + 1;
                }
            }
        }

        // Make sure we have an id
        if (id === undefined) {
            // Get the maximum id so far and increase it
            id = 0;
            var localId;
            for (i = 0; i < this.widgets.length; ++i) {
                localId = parseInt(this.widgets[i].id, 10);
                if (localId >= id) {
                    id = localId + 1;
                }
            }
        }

        var object = { id: id, title: title, widgettype: type, order: order };
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
            LFW_DASHBOARD.opts.config.id = "default-dashboard-id";
        }
        if (!LFW_DASHBOARD.opts.config.title) {
            LFW_DASHBOARD.opts.config.title = "Dashboard";
        }

        this._columns = LFW_DASHBOARD.opts.config.columns;
        this.id = LFW_DASHBOARD.opts.config.id;
        this.title = LFW_DASHBOARD.opts.config.title;
        this.columns = [];
        this.widgetTypes = null;

        // Add the dashboard
        var data = $.tmpl('plugin.dashboard.main', LFW_DASHBOARD.opts.config);
        console.log('Dashboard Rendered: ' + data.html());
        LFW_DASHBOARD.opts.swap($(data).html());
        this.jq = $("#" + this.id);
        var that = this;

        // Make the widget store work
        this.jq.find(".dashboard-header .ui-icon-plusthick").click($.proxy(this.showWidgetStore, this));

        this.jq.find(".dashboard-header .ui-icon-wrench").remove();
        /*this.jq.find(".dashboard-header .ui-icon-wrench").click(function() {
            alert('Configure dashboard');
        });*/

        // Sort the columns by order first
        this._columns.sort(function(col1, col2) {
            if (col1.order !== col2.order) {
                return col1.order < col2.order;
            } else {
                return 0;
            }
        });

        // Create the Columns
        var i;
        for (i = 0; i < this._columns.length; ++i) {
            this.columns.push(new LFW_DASHBOARD.Column(this, this._columns[i], this.jq.width() / this._columns.length));
        }

        // Make the widgets moveable
        this.jq.find(".column").sortable({
            connectWith: ".column"
        });
        this.jq.find(".column").disableSelection();
    }

    // Show the widget store
    Dashboard.prototype.showWidgetStore = function() {
        // Create the widget store if needed
        var widgetStore = $("#widgetStore"),
            that = this,
            search;

        if (!this.widgetTypes) {
            // Load the data first
            $.get("appserver/rest/ui/portal/generic", { tagstring: "", macroname: "macrolist" }, function(data) {
                that.widgetTypes = data;
                that.showWidgetStore();
            });
            return;
        }
        if (widgetStore.length === 0) { //add it
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
                for (i = 0; i < that.widgetTypes.length; ++i) {
                    type = that.widgetTypes[i];

                    // Search name
                    if (contains(type, types)) {
                        widgets.push(type);
                    }
                }

                // Show results
                display.empty();
                for (i = 0; i < widgets.length; ++i) {
                    type = widgets[i];
                    display.append("<div id='widget-" + type + "' class='widgettype'>" +
                        "<img src='img/widget-" + type + ".png' />" +
                        "<button class='add'><span class='ui-button-text'>Pick me</span></button>" +
                        "<h3>" + type + "</h3><p>" +
                        "No description</p></div>");
                }

                // Make em clickable
                display.find(".add").click(function() {
                    type = $(this).parent().attr("id").replace("widget-", "");

                    // Add the widget
                    that.columns[0].addWidget(undefined, "New " + type + " widget", type);

                    widgetStore.dialog("close");
                });
            });
        }

        // Update types
        search = widgetStore.find(".search");
        var typeContainer = widgetStore.find(".types"),
            type;
        typeContainer.empty();
        typeContainer.append("<li title=''>All (" + this.widgetTypes.length + ")</li>");
        for (i = 0; i < this.widgetTypes.length; ++i) {
            type = this.widgetTypes[i];
            typeContainer.append("<li title='" + type +"'>" + type + "</li>");
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

    LFW_DASHBOARD.Dashboard = Dashboard;
});

var render = function(options) {
    LFW_DASHBOARD.opts = options;

    // CSS
    options.addCss({'id': 'dashboardmacro', 'tag': 'style', 'params': '.dashboard { margin: 0px; }' +
        '.dashboard-header { margin: 0.3em; padding-bottom: 4px; padding-left: 0.2em; }' +
        '.dashboard-header .ui-icon { float: right; cursor: pointer; }' +
        '.dashboard .columns .column { margin: 0px; float: left; padding: 10px; }' +
        '.portlet { margin: 0 0 1em 0; position: relative; }' +
        '.portlet-header { margin: 0.3em; padding-bottom: 4px; padding-left: 0.2em; cursor: move; }' +
        '.portlet-header .icons { float: right; display: none; }' +
        '.portlet-header .icons .ui-icon { float: right; cursor: pointer; }' +
        '.portlet .portlet-menu { position: absolute; z-index: 1000; right: 5px; top: 20px; }' +
        '.portlet .portlet-options { background: #DDDDDD; border: 1px solid #AAAAAA; position: relative; ' +
            'overflow:hidden; }' +
        '.portlet .portlet-options div { float: left; }' +
        '.portlet .portlet-options .options-table .options-textnode { vertical-align: middle; }' +
        '.portlet .portlet-options { background-color: #cccccc; }' +
        '.portlet .portlet-options fieldset { border: 1px solid #FFFFFF; margin: 0.5em; padding: 0.5em; }' +
        '.portlet .portlet-options .options-table { width: 100%; height: 100%; margin: 0px; }' +
        '.portlet .portlet-options .options-table td { vertical-align: top; }' +
        '.portlet .portlet-options .options-table .options-title { width: 98%; }' +
        '.portlet .portlet-options .options-buttons { text-align: right; }' +
        '.portlet .portlet-options .options-ok { margin-top: 1.5em; float: right; margin-left: 0.5em; }' +
        '.portlet .portlet-options .options-cancel { margin-top: 1.5em; float: right; }' +
        '.portlet .portlet-content { padding: 0.4em; }' +
        '.portlet .ui-sortable-placeholder { border: 1px dotted black; visibility: visible !important; height: 50px' +
            ' !important; }' +
        '.ui-sortable-placeholder * { visibility: hidden; }' +
        '#widgetStore { font-size: 1.1em; }' +
        '#widgetStore .column-left { width: 22%; float: left; height: 414px; border-right: 1px solid #999;' +
            ' margin-left: -1px; overflow: auto; }' +
        '#widgetStore .column-left .search { width: 90%; font-size: 100%; }' +
        '#widgetStore .column-left li { margin-top: 5px; cursor: pointer; }' +
        '#widgetStore .column-right { width: 78%; float: left; overflow: auto; height: 414px; }' +
        '#widgetStore .column-right .widgettype { padding: 0 20px 0 140px; width: 150px; height: 140px; float: left;' +
            ' overflow: hidden; }' +
        '#widgetStore .column-right .widgettype:hover { background-color: #0071B5; color: #FFFFFF; }' +
        '#widgetStore .column-right .widgettype button { margin: 81px 0 0 -131px; float: left; }' +
        '#widgetStore .column-right .widgettype img { margin: 10px 0 0 -130px; border: 1px solid #999; float: left; ' +
            'width: 120px; height: 60px; }' +
        '#widgetStore .column-right .widgettype h3 { margin: 11px 0 0; }' +
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
                '<div class="dashboard-header ui-widget-header ui-corner-all">' +
                    '<span class="ui-icon ui-icon-plusthick" /><span class="ui-icon ui-icon-wrench" />${title}</div>' +
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
            '<div class="portlet-options">' +
                '<form><table class="options-table">' +
                    '<tr><td class="options-textnode">Title:</td>' +
                    '<td align="left"><input type="text" class="options-title" value="" /></td></tr>' +
                    '<tr><td class="options-textnode">Content:</td>' +
                    '<td align="left"><textarea class="options-content" /></td></tr>' +
                    '<tr><td colspan="2" class="options-buttons">' +
                        '<button class="options-ok"><span class="ui-button-text">Ok</span></button>' +
                        '<button class="options-cancel"><span class="ui-button-text">Cancel</span></button>' +
                    '</td></tr>' +
                '</table></form></div>' +
            '<div class="portlet-content">' +
                '<div class="macro macro_${widgettype}" {{if params}}params="${params}"{{/if}}>${config}</div>' +
            '</div>' +
        '</div>');

    // Create the dashboard
    LFW_DASHBOARD.instance = new LFW_DASHBOARD.Dashboard();
};

register(render);
