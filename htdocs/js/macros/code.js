var render = function(options) {
  $this = $(this);
  
  $.template('plugin.code.highlight', '<div><pre><code>${options}</code></pre></div>');
  var c = $.tmpl('plugin.code.highlight', {'options': options.options});
  
  $this.append(c);

  hljs.tabReplace = '    '; // 4 spaces
  //hljs.tabReplace = '<span class="indent">\t</span>';
  $this.find('pre code').each(function(i, e) {hljs.highlightBlock(e, '    ')});
};

register(render);