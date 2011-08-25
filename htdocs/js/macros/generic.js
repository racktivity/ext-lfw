//@metadata wizard=generic
//@metadata description=Generic widget calling serverside python tasklet
//@metadata documentationUrl=http://www.pylabs.org/#/alkiradocs/MacroGeneric

var render = function(options) {

    var $this = $(this);

    tagstring = $.trim(options.body);

    tagstring = tagstring + ' page:' + options.page;
    tagstring = tagstring + ' space:' + options.space;
    macroname = options.params.macroname || 'generic'

    $.get(
    'appserver/rest/ui/portal/generic',
    {
        tagstring: tagstring,
        macroname: macroname
    },
    'json'
    )
    .success( function (data, textStatus, jqXHR) {
        console.log('Got config: ' + $.toJSON(data));
        options.swap(options.renderWiki(data), '', $this);
    })
    .error( function (data, textStatus, jqXHR) {
        console.log('Failed to get config: ' + textStatus);
    });
};
register(render);

