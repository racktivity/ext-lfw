var render = function(options) {
    var $this = $(this);
    
    var cb = function () {
	    $.template('plugin.code.highlight', '<div><pre><code>${options}</code></pre></div>');
	    var c = $.tmpl('plugin.code.highlight', {'options': options.body});
	  
	    $this.append(c);
	
	    hljs.tabReplace = '    '; // 4 spaces
	    //hljs.tabReplace = '<span class="indent">\t</span>';
	    $this.find('pre code').each(function(i, e) {hljs.highlightBlock(e, '    ')});
	};
    
    options.addCss({'id': 'codemacro', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': 'http://yandex.st/highlightjs/5.16/styles/default.min.css'}})
    options.addDependency(cb, ['http://yandex.st/highlightjs/5.16/highlight.min.js'])
};

register(render);