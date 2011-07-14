//@metadata wizard=graphviz
//@metadata description=Plots graphs like finite state, flowcharts
//@metadata image=img/macros/graphviz.png

var render = function(options) {
    var TEMPLATE_NAME = 'plugin.graphviz';
    var $this = $(this);

    $.ajax({
        type: 'POST',
        url: 'appserver/rest/ui/portal/generic/',
        data: { tagstring: "",
                graphDot_str: options.body,
                macroname: "graphviz"
        },
        success: function (data, textStatus, jqXHR) {
            $.template(TEMPLATE_NAME, '<div><img src="data:image/gif;base64,${data}" alt="Graphviz Image"/></div>');
            $.tmpl(TEMPLATE_NAME, {data:data}).appendTo($this);
        },
        error: function (data, textStatus, jqXHR) {
            console.log('Failed to get config: ' + textStatus);
        }
        });
}

register(render);
