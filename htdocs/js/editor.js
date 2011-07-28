(function($){
    $.fn.editor = function(options){
        var functions = {};

        var filetypes = {'md': "null",
                         'html': "null",
                         'txt': "null",
                         'py': 'python'};

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
        
        functions.filetype = function(type){
            if (typeof type !== "undefined"){
                var mode = (type ? filetypes[type] : "null");
                if ($.inArray(mode, CodeMirror.listModes()) == -1) {
                    console.log("Not supported file type")
                    mode = "null";
                }
                
                return this.each(function() {
                    var editor = $(this).data("editor");
                    editor.setOption("mode", mode);
                });
            } else {
                var mode = $(this).data("editor").getOption("mode");
                var t = null;
                $.each(filetypes, function(k, v){
                    if (v == mode && !type){
                        t = k;
                    }
                });
                
                return t;
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

        

        var layout = "<div class='editor-body'><textarea></textarea></div>";

        var getCandidates = function(token) {
            var candidates = {};
            $.each(autocompletelist, function(i, opt){
                if (opt.indexOf(token) == 0) {
                    var doti = opt.indexOf('.', token.length);
                    if (doti != -1){
                        opt = opt.substring(0, doti);
                    }
                    var optstring = opt.substring(opt.lastIndexOf('.'));
                    if (!(opt in candidates))
                        candidates[opt] = optstring;
                }
            });

            return candidates;
        };

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
                return false;
            }

            var spaceIndex = leftline.lastIndexOf(leftstop[0]);
            var token = leftline.substring(spaceIndex);
            if (token.length < 2) {
                return false;
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
                    var code = e.which;
                    if (code == 27){
                        //escape.
                        e.preventDefault();
                        editor.focus();
                    }else if (code == 8){
                        //backspace.
                        e.preventDefault();
                        e.stopImmediatePropagation();

                        line = line.substring(0, cur.ch - 1) + line.substring(cur.ch);
                        editor.setLine(cur.line, line);
                        editor.focus();
                        startComplete.call(editor, body, event);
                    }
                })
                .keypress(function(e){
                    var code = e.which
                    if (e.ctrlKey) return false;
                    if (code == 13 || code == 32) {
                        //enter and space
                        e.preventDefault();
                        pick.call(this);
                        return true;
                    } else if ($.inArray(code, [0, 8, 27]) < 0) {
                        //continues typing
                        line = line.substring(0, cur.ch) + String.fromCharCode(code) + line.substring(cur.ch);
                        editor.setLine(cur.line, line);
                        editor.focus();
                        return startComplete.call(editor, body, event);
                    }
                    return false;
                });

            var candidates = getCandidates(token);
            if ($.isEmptyObject(candidates)) {
                return false;
            }

            $.each(candidates, function(k, v){
                list.append($("<option>").val(k).text(v));
            });
            //select the first option.
            list.children().first().attr("selected", true);

            var coords = editor.cursorCoords();
            var offset = body.offset();

            var complete = $("<div>", {'class': 'completions'})
                            .append(list).offset({left: coords.x,
                                                  top: coords.yBot});

            body.append(complete);
            
            list.focus();
            return true;
        };
        
        var options = $.extend(true, {filetype: 'md',
                                      content: '',
                                      onchange: $.noop}, options);
        
        var selection = this;
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
                    options.onchange();
                    if (e.keyCode == 32 && (e.ctrlKey || e.metaKey) && !e.altKey) {
                        e.stop();
                        return startComplete.call(editor, $this.find(".editor-body"), e);
                    }
                }});

            $this.data("editor", editor);
            
            functions.filetype.call(selection, "filetype", options.filetype);
        });
    };
})(jQuery);


