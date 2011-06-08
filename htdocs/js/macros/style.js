var render = function(options) {

    var $this = $(this);    
    var body = options.body;
    var src = options.params.src;
    var func = function() {};
    if (src){
        dominoes(src, func);
    }
    if (body){
        var script = $("<script>").text(body);
        $("head").append(script);
    }

}

register(render);
