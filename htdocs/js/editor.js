(function($){
    
    $.fn.editor = function(options){
        var functions = {};
        
        functions.content = function(text) {
            if (text) {
                this.each(function(){
                    $(this).find(".editor").text(text);
                });
            } else {
                return this.find(".editor").text();
            }
        };
        
        functions.option = function(key, value) {
            
        };
        
        if (typeof options === "string"){
            //this is a method call
            var args = [];
            $.each(arguments, function(i, a){
                if (i == 0) return;
                args.push(a);
            });
            var ret = functions[options].apply(this, args);
            if (ret){
                return ret;
            }
            return this;
        }
        
        var options = $.extend(true, {width: '100%',
                                      height: '100%',
                                      type: 'markup',
                                      content: ''}, options);
        return this.each(function(){
            var $this = $(this);
            
            var txtarea = $("<textarea>", {style: "width: 100%; height: 100%; padding: 0px; margin: 0px; border: 1px solid gray;"}).addClass("editor");
            txtarea.text(options.content);
            $this.append($("<div>").css('width', options.width)
                                   .css('height', options.height)
                                   .append(txtarea));
        });
    };
})(jQuery);
