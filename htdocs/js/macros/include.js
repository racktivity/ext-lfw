//@metadata wizard=include
//@metadata ignore=true

var render = function(options) {

    var me = this;
    var space = options.params.space || options.space;
    var name = options.params.name;

    console.log('[macro_include] Retrieving page ' + name + ' from space ' + space);

    // @todo: change to $.swap
    $.getJSON(LFW_CONFIG['uris']['pages'],
        {
            'space': space,
            'name': name
        },
        function(data) {
            $this = $(me);

            rendered = options.renderWiki(data.content);
            options.swap(rendered);
    });
}

register(render);
