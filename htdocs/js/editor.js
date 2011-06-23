(function($){
    
    $.fn.editor = function(options){
        var functions = {};
        
        functions.content = function(text) {
            if (typeof text !== "undefined") {
                return this.each(function(){
                    $(this).find(".editor").val(text);
                });
            } else {
                return this.find(".editor").val();
            }
        };
        /*
        functions.name = function(text) {
            if (text) {
                this.each(function(){
                    $(this).find("#pagename").val(text);
                });
            } else {
                return this.find("#pagename").val();
            }
        };
        */
        functions.title = function(text) {
            if (typeof text !== "undefined") {
                this.each(function(){
                    $(this).find("#pagetitle").val(text);
                });
            } else {
                return this.find("#pagetitle").val();
            }
        };
        
        
        functions.data = function(key, value) {
            return this.data(key, value);
        };
        
        if (typeof options === "string"){
            //this is a method call
            var args = [];
            $.each(arguments, function(i, a){
                if (i == 0) return;
                args.push(a);
            });
            return functions[options].apply(this, args);
        }
        
        var options = $.extend(true, {width: '100%',
                                      height: '100%',
                                      type: 'markup',
                                      content: ''}, options);
        
        var layout = "<div style='width: 100%; height: 100%'>\
    <div id='bar'>\
        <label for='pagetitle'>Page Title: </label>\
        <input id='pagetitle' class='text'>\
    </div>\
    <div id='conent' style=' bottom: 10px; margin-bottom: 0;  display:  block; position: absolute; top: 50px; left: 10px; right: 10px;'>\
        <textarea class='editor' style='width: 100%; height: 100%; padding: 0px; margin: 0px; border: 1px solid gray;'></textarea>\
    </div>\
</div>";
        
        return this.each(function(){
            var $this = $(this);
            $this.html(layout);
            $this.find(".editor").val(options.content);
        });
    };
})(jQuery);


