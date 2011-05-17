var render = function(options) {
    var $this = $(this);
    
    $.template('plugin.page.toc', '<div><div id="toc"></div><div id="content">${options}</div></div>');
    var tocTemplate = $.tmpl('plugin.page.toc', {});
    $this.append(tocTemplate);
    
    var value = "H1, H2, H3, H4, H5, H6";
    var previous = 1;
    var first = true;

    function addAnchor(docURL, headerLink, headerTitle)
    {
        var anchor = "<li><a href='" + docURL + "/#" + headerLink + "'>" + headerTitle + "</a>"
        return anchor
    }

    var toc_string = "<p><b>Table of Contents:</b></p>";
    toc_string += "<ul>";
    
    options.pagecontent.find(value).each(function(i) {
        var current = $(this);
        var headerLink = "header" + i;
        var headerLevel = this.tagName;
        
        current.attr("id", headerLink);
        headerLevel = headerLevel.split("H")[1];
        
        if (headerLevel > previous)
        {
            toc_string += "<ul>";
            toc_string += addAnchor(document.URL, headerLink, current.html())
        }
        else if (headerLevel < previous)
        {
            close_amount = previous - headerLevel;
            for(i=0;i<close_amount;i++)
            {
                toc_string += "</li></ul>";
            }
            toc_string += addAnchor(document.URL, headerLink, current.html())
        }
        else if (headerLevel == previous)
        {
            if (first == true)
            {
                first = false;
            }
            else
            {
                toc_string += "</li>";
            }
            toc_string += addAnchor(document.URL, headerLink, current.html())
        }
        previous = headerLevel;
    });

    for(i=0;i<previous;i++)
    {
        toc_string += "</li></ul>";
    }

    $('#toc').append(toc_string);
}

register(render);
