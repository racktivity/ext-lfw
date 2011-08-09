//@metadata wizard=googlemaps
//@metadata description=Shows Google Maps static map of choice
//@metadata image=img/macros/googlemaps.png
//@metadata documentationUrl=http://www.pylabs.org/#/alkiradocs/MacroGoogleMaps

var render = function(options) {
    var $this = $(this);
    var lat = parseFloat(options.params.latitude) || 51.1;
    var longitude = parseFloat(options.params.longitude) || 3.83333;
    var width = parseFloat(options.params.width) || 250;
    var height = parseFloat(options.params.height) || 250;
    var zoom = parseFloat(options.params.zoom) || 8;

    var cb = function(){
        var latlng = new google.maps.LatLng(lat, longitude);
        var myOptions = {
          zoom: zoom,
          center: latlng,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        };

        var style = 'width:' + width + 'px; height:' + height + 'px';
        var canvas = $('<div>').attr('style', style);
        $this.append(canvas);

        var map = new google.maps.Map(canvas[0], myOptions);
    };

    options.addCss({'id': 'googlemaps', 'tag': 'style', 'params': 'html { height: 100% }\
    body { height: 100%; margin: 0px; padding: 0px }\
    #map_canvas { height: 100% }'});
    options.addDependency(cb, ['http://maps.google.com/maps/api/js?sensor=false', "http://maps.gstatic.com/intl/en_us/mapfiles/api-3/4/2/main.js"], true);
};

register(render);
