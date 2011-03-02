var render = function(options) {
	var $this = $(this);
    
    $.template('plugin.page.toc', '<div><div id="toc"></div><div id="content">${options}</div></div>');
    var tocTemplate = $.tmpl('plugin.page.toc', {});
    $this.append(tocTemplate);
    
    var body = $(options.body);
    value = "h1, h2, h3";
    if (body != undefined) {
    	value = body.attr('value');
    }

    $("#toc").append('<p>Table of Contents:</p>');
    options.pagecontent.find(value).each(function(i) {
        var current = $(this);
        current.attr("id", "title" + i);
        $("#toc").append("<a id='link" + i + "' href='/#/" + options.space + "/" + options.page + "/#title" +
            i + "'>" + current.html() + "</a><br />");
    });
}

register(render);
