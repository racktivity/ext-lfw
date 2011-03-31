var render = function(options) {
    var TEMPLATE_NAME = 'plugin.graphviz';
    var $this = $(this);

    $.ajax({
        type: 'POST',
        url: '/appserver/rest/lfw/graphviz/',
        data: {graphDot_str: options.body},
        success: function (data, textStatus, jqXHR) {
            console.log('Got data: ' + data);
            $.template(TEMPLATE_NAME, '<div><img src="${data}" alt="some_text"/></div>');
            $.tmpl(TEMPLATE_NAME, {data:data}).appendTo($this);
        },
        error: function (data, textStatus, jqXHR) {
            console.log('Failed to get config: ' + textStatus);
        }
        });
}

register(render);