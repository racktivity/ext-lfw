var render = function(options) {
	var $this = $(this);
    
    $.template('plugin.page.toc', '<div><div id="toc"></div><div id="content">${options}</div></div>');
    var tocTemplate = $.tmpl('plugin.page.toc', {});
    $this.append(tocTemplate);
    
    var value = "H1, H2, H3, H4, H5, H6";
    var toc_ul = $('<ul>');

    $("#toc").append('<p><b>Table of Contents:</b></p>');
    options.pagecontent.find(value).each(function(i) {
        var current = $(this);
        var headerLink = "header" + i;
        current.attr("id", headerLink);

        if (this.tagName == 'H1') {
            toc_ul.append("<li><a id='link" + i + "' href='" + document.URL + "/#" + headerLink + "'>" + current.html() + "</a></li>");
            toc_ul.append('&nbsp;');
        }
        else if (this.tagName == 'H2') {
            toc_ul.append("<ul><li><a id='link" + i + "' href='" + document.URL + "/#" + headerLink + "'>" + current.html() + "</a></li></ul>");
        }
        else if (this.tagName == 'H3') {
            toc_ul.append("<ul><ul><li><a id='link" + i + "' href='" + document.URL + "/#" + headerLink + "'>" + current.html() + "</a></li></ul></ul>");
        }
        else if (this.tagName == 'H4') {
            toc_ul.append("<ul><ul><ul><li><a id='link" + i + "' href='" + document.URL + "/#" + headerLink + "'>" + current.html() + "</a></li></ul></ul></ul>");
        }
        else if (this.tagName == 'H5') {
            toc_ul.append("<ul><ul><ul><ul><li><a id='link" + i + "' href='" + document.URL + "/#" + headerLink + "'>" + current.html() + "</a></li></ul></ul></ul></ul>");
        }
        else if (this.tagName == 'H6') {
            toc_ul.append("<ul><ul><ul><ul><ul><li><a id='link" + i + "' href='" + document.URL + "/#" + headerLink + "'>" + current.html() + "</a></li></ul></ul></ul></ul></ul>");
        }

    });
    $('#toc').append(toc_ul);
}

register(render);
