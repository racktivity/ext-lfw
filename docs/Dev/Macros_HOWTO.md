## How to create Macros

###  Example macro to show google map

<div class="macro macro_code">
	var render = function(options) {
	    var $this = $(this);
	
	        var cb = function(){
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
</div>


1. Create a macro file under /opt/qbase3/www/js/macros/macrofilename.js (lets call the file macrotest.js)

2. There must be a render function which takes options as a parameter. Options is an object with some parameters that we can use, such as:
    * __options.space:__ Gets space name.
    * __options.page:__ Gets page name.
    * __options.body:__ Gets the page contents.
    * __options.addCss():__ Function to set CSS style sheet either through a CSS file or a direct style code.
    * __options.addDependency():__ Function to add a javascript library dependency if needed by the macro.
    * __options.swap():__ Function to swap the old contents of a page with new ones.
    * __options.renderWiki():__ Function to return the HTML element of given markdown syntax.  
       
3. If your macro needs to add special style sheet, you need to use options.addCss() function which takes an object with:
    * __id:__ a unique id for your macro (usually just the macro name since it should be unique).
    * __tag:__ either "style" or "link" tag, where:

        * *style:* is used if you're giving it CSS dumped syntax.
        * *link:* is used if you're giving it a CSS file to load.  
     
    * __params:__

        * if the tag is style, params is a dumped CSS string.
        * if the tag is link, params is an object with key-value.

        For example: 'params': {'rel': 'stylesheet', 'href': 'http://yandex.st/highlightjs/5.16/styles/default.min.css'}

4. If your macro needs to load first one or more javascript libraries that it depends on, then you need to load them with options.addDependency:

    options.addDependency(callback, dependencies):

    * __callback:__ A callback function to be called after loading all dependency scripts.
    * __dependencies:__ Array of file links to be loaded.


    In this case, you have to put all code that depends on the loaded dependencies in a callback function which you give as first argument to the addDependency function call as shown in the example code.

5. Create a template using jquery; jQuery.template(name, template) where:
    * __name:__ A string naming the compiled template.
    * __template:__ The HTML markup and/or text to be used as template. Can be a string, or an HTML element (or jQuery object wrapping an element) whose content is to be used as a template.  
        
6. Render the specified HTML content as a template, using the specified data:

    jQuery.tmpl(name, [ options ]) where:

    * __name:__ A string naming the compiled template.
    * __options:__ An optional map of user-defined key-value pairs. Extends the tmplItem data structure, available to the template during rendering.  
      
7. Register the render function via register(render).

8. Define your macro in a markdown file 
##### Example:

	    <div class="macro macro_macrotest">
	        macro body code goes here
	    </div>
