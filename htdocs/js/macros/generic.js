//@metadata wizard=generic

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
        /** @todo: Should be handled by framework or utility function **/
        var compiler = new Showdown.converter(),
                rendered = compiler.makeHtml(data || '');
        /** /@todo **/
        //$.swap(rendered, '', $this);
        $this.append(rendered);
    })
    .error( function (data, textStatus, jqXHR) {
        console.log('Failed to get config: ' + textStatus);
    });
};
register(render);

