//@metadata wizard=note
//@metadata description=Presents a text "note style"
//@metadata image=img/macros/note.png
//@metadata documentationUrl=http://www.pylabs.org/#/alkiradocs/MacroNote

var render = function(options) {
    var $this = $(this);
    var data  = options.body;
    var rendered = options.renderWiki(data);
    $this.empty();
    $this.addClass("notice");
    $this.append(rendered);
}
register(render);
