//@metadata wizard=pagetree
//@metadata ignore=true

var render = function(options) {

    var TEMPLATE_NAME = 'plugin.page.treeview';
    var $this = $(this);
    var space = options.params.space || options.space;
    var page = options.page;
    var root = options.params.root || 0;
    var lazyload = options.params.lazyload || true;

    options.addCss({'id': 'pagetree', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': 'js/libs/jstree/themes/classic/style.css'}});

    var cb = function(){

        $this.jstree({
            "json_data": {
                "ajax": {
                    "url": "appserver/rest/ui/portal/generic?macroname=pagetree&space=" + space + "&lazyload=" + lazyload,
                    "data": function(n) {
                        return {id: n.attr ? n.attr("id") : root};
                    },
                "progressive_render" : true
                }
            },
            "themes" : {
               "theme" : "classic",
            },
            "plugins": ["themes", "json_data", "cookies", "ui"],
            "cookies": {"save_selected": false}
        })
        .bind("select_node.jstree", function (e, data) {
            var href = data.rslt.obj.children("a").attr("href");
            document.location.href = href;
          });

    }

    options.addDependency(cb, ["js/libs/jstree/jquery.cookie.js", "js/libs/jstree/jquery.hotkeys.js", "js/libs/jstree/jquery.jstree.js"]);
};

register(render);
