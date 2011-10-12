var render = function(options) {
    var $this = $(this);
    var params = $.extend({package: 'default'},
                            options.params);
    
    var value = $.language(params.key, options);
    if (value == params.key){
        value = options.body;
    }
    
    $this.empty();
    $this.text(value);
}
register(render);
