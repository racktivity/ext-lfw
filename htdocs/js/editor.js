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
                                      content: '',
                                      autocomplete: []}, options);
        
        var layout = "<div class='editor'>\
    <div id='editorbar'>\
        <label for='title'>Page Title: </label>\
        <input id='title' class='text'>\
    </div>\
    <div class='body'>\
        <textarea></textarea>\
    </div>\
</div>";

        var startComplete = function(body, event){
            var editor = this;
            if (editor.somethingSelected())
                return;
            
            //Find the token at the cursor
            var cur = editor.getCursor(false);
            var line = editor.getLine(cur.line);
            var leftpatt = /[^\s=\[\]\(\)\:]+$/;
            var rightpatt = /^[^\s=\[\]\(\)\:]+/;
            var leftline = line.substring(0, cur.ch);
            var rightline = line.substring(cur.ch);
            
            //extract the token, find the first stop character from right.
            var leftstop = leftpatt.exec(leftline);
            if (!leftstop) {
                return;
            }
            
            var spaceIndex = leftline.lastIndexOf(leftstop[0]);
            var token = leftline.substring(spaceIndex);
            if (token.length < 3){
                return;
            }
            //get available options.
            
            var hide = function(){
                $(this).parent().remove();
            };
            
            var pick = function(){
                var value = $(this).val()[0];
                var rightstop = rightpatt.exec(rightline);
                if (rightstop){
                    rightline = rightline.substring(rightstop[0].length);
                }
                line = leftline.substring(0, spaceIndex) + value;
                var pos = line.length;
                line = line + rightline;
                editor.setLine(cur.line, line);
                editor.setCursor(cur.line, pos);
                $(this).blur();
                editor.focus();
            };
            
            var list = $("<select>", {'multiple': true})
                .blur(hide)
                .dblclick(pick)
                .keydown(function(e){
                    var code = e.keyCode
                    if (code == 13 || code == 32) {
                        //enter and space
                        event.stop();
                        pick.call(this);
                    }
                    else if (code == 27){
                        //escape
                        event.stop();
                        editor.focus();
                    }
                    /*else if (code != 38 && code != 40) {
                        //not UP or DOWN, then the developer still typing
                        //we need to pass this char to the 
                        line = line.substring(0, cur.ch) + String.fromCharCode(e.which) + line.substring(cur.ch);
                        editor.setLine(cur.line, line);
                        editor.focus();
                        startComplete.call(editor);
                    }*/
                });
            
            var options = [];
            $.each(autocompletelist, function(i, v){
                if (v.indexOf(token) == 0){
                    options.push(v);
                }
            });
            
            if (!options.length) {
                return;
            }
            
            $.each(options, function(i, v){
                list.append($("<option>").val(v).text(v).attr("selected", i == 0));
            });
            
            var coords = editor.cursorCoords();
            var offset = body.offset();
            
            var complete = $("<div>", {'class': 'completions'})
                            .append(list)
                            .css('left', (coords.x - offset.left) + "px")
                            .css('top', (coords.yBot - offset.top) + "px");
            
            body.append(complete);
            list.focus();
        };
        
        return this.each(function(){
            var $this = $(this);
            $this.html(layout);
            
            //initialize codemirror editor
            var editor = CodeMirror.fromTextArea($this.find("textarea")[0],
                {value: options.content,
                indentUnit: 4,
                lineNumbers: true,
                gutter: true,
                theme: 'neat',
                onKeyEvent: function(editor, e) {
                    // Hook into ctrl-space
                    if (e.keyCode == 32 && (e.ctrlKey || e.metaKey) && !e.altKey) {
                        e.stop();
                        return startComplete.call(editor, $this.find(".editor .body"), e);
                    }
                }});
                
            $this.data("editor", editor);
            //set file type.
            functions.filetype.call($this, options.filetype);
        });
    };
})(jQuery);


