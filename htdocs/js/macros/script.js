//@metadata ignore=true

var render = function(options) {

    var $this = $(this);
    var body = options.body;
    var src = options.params.src;
    
    var func = function() {
        if (body){
            var script = $("<script>").text(body);
            $("head").append(script);
        }
    };
    
    if (src){
        dominoes(src, func);
    } else {
        func();
    }
}

register(render);
