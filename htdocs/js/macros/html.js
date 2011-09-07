//@metadata description=Add html elements to the document

var render = function(options) {
    var $this = $(this);
    var data  = options.body;
    $this.empty();
    $this.html(data);
}
register(render);
