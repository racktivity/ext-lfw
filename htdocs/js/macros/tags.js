//@metadata description=Shows page tags
//@metadata image=img/macros/tags.png

var render = function(options) {
    var $this = $(this);
    
    var body = $("<div>", {'class': 'tags-body'})
                    .append($("<span>", {'class': 'tags-label'}).text("Tags:"))
                    .append($("<span>", {'class': 'tags-content'}).text(options.tags.join(" ")));

    options.addCss({'id': 'tags', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': 'css/macros/tags.css'}});
    $(this).empty().append(body);
};

register(render);
