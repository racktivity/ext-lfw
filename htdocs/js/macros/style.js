//@metadata ignore=true

var render = function(options) {

    var $this = $(this);
    var body = options.body;
    var src = options.params.src;
    var func = function() {};
    if (src){
        dominoes("$css(" + src + ")", func);
    }
    if (body){
        var script = $("<style>").text(body);
        $("head").append(script);
    }

}

register(render);
