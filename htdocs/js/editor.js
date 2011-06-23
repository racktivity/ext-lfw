(function($){
    
    $.fn.editor = function(options){
        var functions = {};
        
        functions.content = function(text) {
            if (text) {
                this.each(function(){
                    $(this).find(".editor").val(text);
                });
            } else {
                return this.find(".editor").val();
            }
        };
        
        functions.name = function(text) {
            if (text) {
                this.each(function(){
                    $(this).find(".pagename").val(text);
                });
            } else {
                return this.find(".pagename").val();
            }
        };
        
        functions.title = function(text) {
            if (text) {
                this.each(function(){
                    $(this).find(".pagetitle").val(text);
                });
            } else {
                return this.find(".pagetitle").val();
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
            var name = $("<input>", {style: 'height: 25px; padding: 0px; margin-bottom: 5px; border: 1px solid gray;'}).addClass("pagename");
            var title = $("<input>", {style: 'height: 25px; padding: 0px; margin-bottom: 5px; border: 1px solid gray;'}).addClass("pagetitle");
            txtarea.val(options.content);
            
            
            $this.append($("<div>").css('width', options.width)
                                   .css('height', options.height)
                                   .append($("<label>").text("Name:"))
                                   .append(name)
                                   .append($("<label>").text("Title:"))
                                   .append(title)
                                   .append(txtarea));
            
            
        });
    };
})(jQuery);

<div>
    <div id='bar'>
        <label for='pagename'>
        <input id='pagename'>
        <label for='pagetitle'>
        <input id='pagetitle'>
    </div>
    <div id='conent'>
        <textarea class='editor'></textarea>
    </div>
</div>
