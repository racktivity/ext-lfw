(function($){
    $.alert = function(message, options) {
        var options = $.extend({title: ''}, options);
        $("<div>").append($("<p>").html(message))
            .dialog({modal: true,
                     width: 600,
                     resizable: false,
                    title: options.title,
                    buttons: {Ok: function(){
                       $(this).dialog("close");
                    }}});
    };
    
    $.alerterror = function(xhr, text, exc, options){
        var options = $.extend({title: 'Error'}, options);
        
        var message = "";
        if(xhr.status === 404) {
            message = "Not Found";
        }
        else if (xhr.status === 401){
            message = "<p class='error'> Invalid UserName/Password</p>";
        }
        else if (xhr.status === 500) {
            var response = $.parseJSON(xhr.responseText);
            message = "<p class='error'>" + response.exception + "</p>";
        }
        else if (xhr.responseText.indexOf("Authorization failed") > 0){
          message = "<p class='error'> Authorization failed</p>";
        }
        else {
            app.error('Unknown error: ' + text, exc);
        }
        $.alert(message, options);
    };
    
    $.confirm = function(message, options) {
        var options = $.extend({title: '',
                                ok: $.noop}, options);
                                
        $("<div>").append($("<p>").text(message))
            .dialog({modal: true,
                    title: options.title,
                    buttons: {Ok: function(){
                                options.ok();
                                $(this).dialog("close");
                                },
                            Cancel: function(){
                                $(this).dialog("close");
                                }}
                    });
    };
    
})(jQuery);
