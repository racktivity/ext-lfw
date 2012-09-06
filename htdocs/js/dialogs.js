(function($) {
    $.alert = function(message, options) {
        var opts = $.extend({
            title: '',
            width: 600
        }, options);
        $("<div>").append(
            $("<p>").html(message))
                .dialog({
                    modal: true,
                    width: opts.width,
                    resizable: false,
                    title: opts.title,
                    buttons: {
                        Ok: function() {
                            $(this).dialog("destroy").remove();
                        }
                    }
                });
    };

    $.alerterror = function(xhr, text, exc, options) {
        var opts = $.extend({ title: 'Error' }, options);

        var message = "";
        if (xhr.status === 404) {
            message = "Not Found";
        }
        else if (xhr.status === 401) {
            message = "<p class='error'> Invalid UserName/Password</p>";
        }
        else if (xhr.status === 500) {
            var response = $.parseJSON(xhr.responseText);
            message = "<p class='error'>" + response.exception + "</p>";
        }
        else if (xhr.responseText.indexOf("Authorization failed") > 0) {
            message = "<p class='error'> Authorization failed</p>";
        }
        else {
            message = "Unkown error: " + text + " - " + exc;
        }
        $.alert(message, opts);
    };

    $.confirm = function(message, options) {
        var opts = $.extend({ title: '', ok: $.noop }, options);

        $("<div>").append($("<p>").text(message))
            .dialog({
                modal: true,
                title: opts.title,
                buttons: {
                    Ok: function() {
                        opts.ok();
                        $(this).dialog("destroy").remove();
                    },
                    Cancel: function() {
                        $(this).dialog("destroy").remove();
                    }
                }
            });
    };

    $.prompt = function(message, options) {
        var opts = $.extend({
            title: '',
            value: '',
            pattern: /.*/,
            error: "Invalid Input",
            ok: $.noop
        }, options);

        var dialog = $("<div>").append($("<p>").text(message))
            .append($("<input id='input' style='width: 100%'>").val(opts.value))
                .dialog({
                    modal: true,
                    title: opts.title,
                    buttons: {
                        Ok: function() {
                            var input = dialog.find("#input").val();
                            if (opts.pattern.test(input)) {
                                opts.ok(input);
                                $(this).dialog("close");
                            } else {
                                $.alert(opts.error, {title: "Invalid Input"});
                            }
                        },
                        Cancel: function() {
                            $(this).dialog("close");
                        }
                    },
                    close: function() {
                        $(this).dialog("destroy").remove();
                    }
                });
    };

})(jQuery);
