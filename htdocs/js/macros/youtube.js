var render = function(options) {
  $this = $(this);
  
  var config = {
    movieid: options.params.movieid || "grbSQ6O6kbs",
    width: options.params.width || "270",
    height: options.params.height || "227"
  };    
  
  $.template('plugin.youtube.content', '<div><iframe title="YouTube video player" width="${width}" height="${height}" src="http://www.youtube.com/embed/${movieid}" frameborder="0" allowfullscreen></iframe></div>');
  $.tmpl('plugin.youtube.content', config).appendTo($this);
}

register(render)
