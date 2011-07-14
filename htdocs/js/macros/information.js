//@metadata wizard=information
//@metadata description=Presents a text "information style"
//@metadata image=img/macros/information.png

var render = function(options) {
    var $this = $(this);
    var data  = options.body;
    var rendered = options.renderWiki(data);
    $this.empty();
    $this.addClass("info");
    $this.append(rendered);
}
register(render);
