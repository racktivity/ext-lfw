var render = function(options) {

    var $this = $(this);
    var defaultmsg = $("<div>").html("The curent page is out of date click <a href=\"javascript:location.reload();\">here</a> to reload.");
    var params = $.extend({content: defaultmsg, delay:-1, cssclass: "customNotify"}, options.params);
    params.delay = Number(params.delay);
    $this.addClass(params.cssclass);
    $this.html(params.content);

    var tagstring = $.trim(options.body);
    var updatetime = options.pageobj.creationdate;

    tagstring += ' page:' + options.page;
    tagstring += ' space:' + options.space;
    var timetagstring = tagstring + ' updatetime:' + updatetime;
    
    function checkupdate(){
        $.ajax({
            url:   'appserver/rest/ui/portal/generic',
            data: {
                tagstring: timetagstring,
                macroname: "notification"
              },
            dataType: 'json',
            global: false,
            success: function (data, textStatus, jqXHR) {
                        checkupdate();
                        if (data > updatetime){
                            updatetime = data;
                            timetagstring = tagstring + ' updatetime:' + updatetime;
                            $this.jmNotify({delay:params.delay});
                        }
                      },
            error:   function (data, textStatus, jqXHR) {
                        checkupdate();
                     }
        });

    };

    function cb(){
        checkupdate();
    }
    options.addCss({'id': 'jmNotify', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': 'css/jmNotify.css'}});
    options.addDependency(cb, ["js/libs/jquery.jmNotify.js"]);
};
register(render);

