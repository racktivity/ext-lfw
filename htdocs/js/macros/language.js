var render = function(options) {
    var $this = $(this);
    var params = $.extend({package: 'default',
                           wiki: 'false'},
                            options.params);
    
    var wiki = JSON.parse(params.wiki);
    
    var value = $.language(params.key, options);
    if (value == params.key){
        value = options.body;
    }
    
    $this.empty();
    if (wiki){
        $this.html(options.renderWiki(value));
    }else{
        $this.text(value);
    }
}
register(render);
