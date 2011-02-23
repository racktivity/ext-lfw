var render = function(options) {
    $this = $(this); 
    
    var latlng = new google.maps.LatLng(51.1, 3.833333);
	var myOptions = {
	  zoom: 8,
	  center: latlng,
	  mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	
    $.template('plugin.googlemaps.content', '<div><div id="map_canvas" style="width:250px; height:250px"></div></div>');
    var result = $.tmpl('plugin.googlemaps.content', myOptions);
    result.appendTo($this);

	var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

};

register(render);
