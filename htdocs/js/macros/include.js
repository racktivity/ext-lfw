var render = function(options) {

    var me = this;    
    config = $.parseJSON(options.body)
    var space = config['space'] || options.space;
    var name = config['name'];
    
    console.log('[macro_include] Retrieving page ' + name + ' from space ' + space);

    // @todo: change to $.swap
    $.getJSON(LFW_CONFIG['uris']['pages'], 
        {
            'space': space,
            'name': name
        },
        function(data) {
            $this = $(me);
            
            /** @todo: Should be handled by framework or utility function **/         
            var compiler = new Showdown.converter(),
                    rendered = compiler.makeHtml(data.content || '');
            /** /@todo **/
                    
            $this.append(rendered);
    });
}

register(render);
