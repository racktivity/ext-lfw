//@metadata description=Add html elements to the document

var render = function(options) {
    var $this = $(this);
    var url = options.body;
    $this.empty();
    //Strip quotes
    width = 800;
    height = 600;
    left = screen.width - width;
    url = String(url).replace(/^('|"|\s)+|('|"|\s)+$/g, '');
    script = 'window.open("' + url + '", "_blank", "toolbar=0, location=0, menubar=0, left=' + left + ', width=' + width + ', height=' + height + '");return false;';
    data = "<div class='macro-helpbutton'><a href='" + url + "' onclick='" + script + "'><img src='img/help.png' border='0'></img><a/></div>";
    this.innerHTML = data;
}
register(render);
