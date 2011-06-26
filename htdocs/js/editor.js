(function($){
    $.fn.editor = function(options){
        var functions = {};
        
        functions.content = function(text) {
            if (typeof text !== "undefined") {
                return this.each(function(){
                    var editor = $(this).data("editor");
                    editor.setValue(text);
                });
            } else {
                var editor = $(this).data("editor");
                return editor.getValue(text);
            }
        };
        
        functions.title = function(text) {
            if (typeof text !== "undefined") {
                this.each(function(){
                    $(this).find("#title").val(text);
                });
            } else {
                return this.find("#title").val();
            }
        };
        
        functions.disabled = function(component, value){
            return this.find("#" + component).attr("disabled", value);
        };
        
        functions.filetype = function(type){
            if (typeof type !== "undefined") {
                type = type === "markup" ? null : type;
                if ($.inArray(type, CodeMirror.listModes()) == -1) {
                    console.log("Not supported file type")
                    type = null;
                }
                
                return this.each(function() {
                    var editor = $(this).data("editor");
                    editor.setOption("mode", type);
                });
            } else {
                var editor = $(this).data("editor");
                return editor.getOption("mode");
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
        
        var options = $.extend(true, {filetype: 'markup',
                                      content: ''}, options);
        
        var layout = "<div style='width: 100%; height: 100%'>\
    <div id='bar'>\
        <label for='title'>Page Title: </label>\
        <input id='title' class='text'>\
    </div>\
    <div style=' bottom: 10px; margin-bottom: 0;  display:  block; position: absolute; top: 50px; left: 10px; right: 10px;'>\
        <textarea id='content' class='editor' style='width: 100%; height: 100%; padding: 0px; margin: 0px; border: 1px solid gray;'></textarea>\
    </div>\
</div>";
        
        return this.each(function(){
            var $this = $(this);
            $this.html(layout);
            
            //initialize codemirror editor
            var editor = CodeMirror.fromTextArea($this.find("textarea")[0],
                {value: options.content,
                indentUnit: 4,
                lineNumbers: true,
                gutter: true,
                theme: 'neat'});
            $this.data("editor", editor);
            
            //set file type.
            functions.filetype.call($this, options.filetype);
        });
    };
})(jQuery);


