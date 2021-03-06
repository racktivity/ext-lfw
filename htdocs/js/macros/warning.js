//@metadata wizard=warning
//@metadata description=Presents a text "warning style"
//@metadata image=img/macros/warning.png
//@metadata documentationUrl=http://www.pylabs.org/#/alkiradocs/MacroWarning

var render = function(options) {
    var $this = $(this);
    var data  = options.body;
    var rendered = options.renderWiki(data);
    $this.empty();
    $this.addClass("error");
    $this.append(rendered);
}
register(render);
