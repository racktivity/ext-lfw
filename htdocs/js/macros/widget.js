//@metadata description=Show a collapseable block with the given content
//@metadata image=img/macros/widget.png
//@metadata documentationUrl=http://www.pylabs.org/#/alkiradocs/MacroWidget

var render = function(options) {
    var $this = $(this);
    var params = $.extend({title: '',
                           width: '',
                           height: '',
                           toggle: 'true',
                           closed: 'false'}, options.params);

    var body = $("<div>", {'class': 'widget-body'});


    var titlebar = $("<div>", {'class': 'widget-titlebar'})
        .append($("<div>", {'class': 'widget-title'}).text(params.title));
        
    if ($.parseJSON(params.toggle)) {
        titlebar.append($("<div>", {'class': 'widget-collapse ui-icon ui-icon-circle-minus'})
            .click(function() {
                var btn = $(this);
                btn.parents(".widget-body").find(".widget-content").slideToggle("fast", function(){
                    if ($(this).css("display") === "none"){
                        btn.removeClass("ui-icon-circle-minus").addClass("ui-icon-circle-plus");
                    } else {
                        btn.removeClass("ui-icon-circle-plus").addClass("ui-icon-circle-minus");
                    }
                });
            }));
    }

    var content = $("<div>", {'class': 'widget-content'})
        .html(options.renderWiki(options.body))
        .css('width', params.width)
        .css('height', params.height);

    body.append(titlebar).append(content);
    options.addCss({'id': 'widget', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': 'css/macros/widget.css'}});
    $this.empty();
    options.swap(body, undefined, true);
    
    if ($.parseJSON(params.closed)) {
        titlebar.find(".widget-collapse").click();
    }
};

register(render);
