//@metadata wizard=tip
//@metadata description=Presents a text "tip style"
//@metadata image=img/macros/tip.png
//@metadata documentationUrl=http://www.pylabs.org/#/alkiradocs/MacroTip

var render = function(options) {
    var $this = $(this);
    var data  = options.body;
    var rendered = options.renderWiki(data);
    $this.empty();
    $this.addClass("success");
    $this.append(rendered);
}
register(render);
