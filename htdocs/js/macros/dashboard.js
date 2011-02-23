var render = function(options) {

    var $this = $(this);
    var space = options.space;
    var name = options.name;

    var default_config = {
        id: "dashboard1",
        title: "My Dashboard",

        colums: [
        {
            order: 0,
            widgets: [
            {
                id: "widget1",
                title: "Widget 1",
                widgettype: "include",
                order: 0
            },
            {
                id: "widget2",
                title: "Widget 2",
                widgettype: "actions",
                order: 1
            },
            ]
        },
        {
            order: 1,
            widgets: [
            {
                id: "widget3",
                title: "Widget 3",
                widgettype: "include",
                order: 0
            },
            {
                id: "widget4",
                title: "Widget 4",
                widgettype: "actions",
                order: 1
            },
            ]
        }
        ]
    };

    // Get config
    var config = $.parseJSON(options.body);

    // @hack: config to json string
    for (var column in config.columns)
        for (var widget in config.columns[column].widgets)
            config.columns[column].widgets[widget].config = $.toJSON(config.columns[column].widgets[widget].config);

    // Define templates
    // @todo: Check if templates are already compiled
    $.template('plugin.dashboard.column', '{{each columns}}<div id="column${order}" class="column">{{each widgets}}<div id="${id}" class="portlet"><div class="portlet-header">${title}</div><div class="portlet-content"><div class="macro macro_${widgettype}">${config}</div></div></div>{{/each}}</div>{{/each}}');
    $.template('plugin.dashboard.main', '<div class="bogus"><div class="dashboard"><div class="dashboard-header">${title}</div><div class="columns">{{tmpl "plugin.dashboard.column"}}</div></div></div>');

    var c = $.tmpl('plugin.dashboard.main', config);

    console.log('Dashboard Rendered: ' + c.html());
    $.swap($(c).html(), '', $this);
    //$this.append(c.html());

    $( function() {
        $( $this )
        .find( ".dashboard" )
        .addClass( "ui-widget ui-widget-content ui-helper-clearfix ui-corner-all" )
        .find( ".dashboard-header" )
        .addClass( "ui-widget-header ui-corner-all" )
        .prepend( "<span class='ui-icon ui-icon-wrench'></span>")
        .prepend( "<span class='ui-icon ui-icon-disk'></span>")
        .prepend( "<span class='ui-icon ui-icon-plusthick'></span>")
        .end();

        $( $this )
        .find( ".dashboard-header .ui-icon-plusthick" ).click( function() {
            alert('Add widget');
        });
        $( $this )
        .find( ".dashboard-header .ui-icon-disk" ).click( function() {
            alert('Save dashboard');
        });
        $( $this )
        .find( ".dashboard-header .ui-icon-wrench" ).click( function() {
            alert('Configure dashboard');
        });
        $( $this )
        .find( ".column" ).sortable({
            connectWith: ".column"
        });

        $( $this )
        .find( ".portlet" ).addClass( "ui-widget ui-widget-content ui-helper-clearfix ui-corner-all" )
        .find( ".portlet-header" )
        .addClass( "ui-widget-header ui-corner-all" )
        .prepend( "<span class='ui-icon ui-icon-wrench'></span>")
        .prepend( "<span class='ui-icon ui-icon-minusthick'></span>")
        .end()
        .find( ".portlet-content" );

        $( $this )
        .find( ".portlet-header .ui-icon-minusthick" ).click( function() {
            $( this ).toggleClass( "ui-icon-minusthick" ).toggleClass( "ui-icon-plusthick" );
            $( this ).parents( ".portlet:first" ).find( ".portlet-content" ).toggle();
        });
        $( $this )
        .find( ".portlet-header .ui-icon-wrench" ).click( function() {

            var widget = $( this ).parents( ".portlet:first" )[0];
            alert('Configure widget ' + widget.id);
        });
        $( $this )
        .find( ".column" ).disableSelection();
    });
};
register(render);
