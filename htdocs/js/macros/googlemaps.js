var render = function(options) {
    var $this = $(this);
 
	var cb = function(){
		console.log('in the callback');
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

    options.addCss({'id': 'googlemaps', 'tag': 'style', 'params': 'html { height: 100% }\
    body { height: 100%; margin: 0px; padding: 0px }\
    #map_canvas { height: 100% }'})
    options.addDependency(cb, ['http://maps.google.com/maps/api/js?sensor=false', "http://maps.gstatic.com/intl/en_us/mapfiles/api-3/4/2/main.js"]);
};

register(render);
