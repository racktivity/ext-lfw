//@metadata wizard=graphviz
//@metadata description=Plots graphs like finite state, flowcharts
//@metadata image=img/macros/graphviz.png
//@metadata documentationUrl=http://www.pylabs.org/#/alkiradocs/MacroGraphViz

var render = function(options) {
    var TEMPLATE_NAME = 'plugin.graphviz';
    var $this = $(this);
    graphDotString = options.body;

    if (!graphDotString) {
        graphDotString = "digraph \"empty\"{}";
    }
    $.ajax({
        type: 'POST',
        url: 'appserver/rest/ui/portal/generic/',
        data: { tagstring: "",
                graphDot_str: graphDotString,
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
