#How to Create Macros
This tutorial will walk you through creating an Alkira macro while using the Google Maps macro as a reference.


##Google Maps Macro Code
Below you can find an example of a macro that shows a static Google map.


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
    	                                                                   #map_canvas { height: 100% }'\
    	                   })
    	    options.addDependency(cb, ['http://maps.google.com/maps/api/js?sensor=false', "http://maps.gstatic.com/intl/en_us/mapfiles/api-3/4/2/main.js"]);
    	};
    	
    	register(render);
    </div>

##Creating a Macro

1. Create a macro file under `/opt/qbase5/www/lfw/js/macros/`, for example `macrotest.js`.

    __Note:__ `lfw` is the acronym for _Lightning Fast Wiki_, which is the Incubaid code name for [Alkira](/sampleapp/#/alkiradocs/Home)

2. There must be a render function which takes `options` as a parameter. Options is an object with some parameters that we can use, such as:
    * __options.space:__ get space name.
    * __options.page:__ get page name.
    * __options.body:__ get the page contents.
    * __options.addCss():__ select a CSS style sheet either through a CSS file or a direct style code.
    * __options.addDependency():__ add a JavaScript library dependency if needed by the macro.
    * __options.swap():__ swap the old content of a page with new content.
    * __options.renderWiki():__ return the HTML element of a given Markdown syntax.  
       
3. If you want to apply a special style sheet for your macro, you need the `options.addCss()` function. This function has three arguments:
    * __id:__ a unique id for your macro (usually just the macro name since it should be unique).
    * __tag:__ either "style" or "link" tag, where:

        * *style:* is used if you're giving it CSS dumped syntax.
        * *link:* is used if you're giving it a CSS file to load.  
     
    * __params:__

        * if the tag is style, params is a dumped CSS string (as shown in the example).
        * if the tag is link, params is a key/value object.

        For example: 'params': {'rel': 'stylesheet', 'href': 'http://yandex.st/highlightjs/5.16/styles/default.min.css'}

4. You can load extra JavaScript libraries in your macro with the `options.addDependency` function. This functions requires two arguments:

    * __callback:__  callback function to be called after loading all dependency scripts, `cb` in the given example
    * __dependencies:__ list of file links to be loaded.

    In this case, you have to put all code that depends on the loaded dependencies in a callback function which you give as first argument to the `addDependency` function call.

5. Create a template using jQuery; jQuery.template(name, template) where:

    * __name:__ A string naming the compiled template.
    * __template:__ The HTML markup and/or text to be used as template. Can be a string, or an HTML element (or jQuery object wrapping an element) whose content is to be used as a template.  
        
6. Render the specified HTML content as a template, using the specified data:

    jQuery.tmpl(name, [ options ]) where:

    * __name:__ A string naming the compiled template.
    * __options:__ An optional map of user-defined key-value pairs. Extends the tmplItem data structure, available to the template during rendering.  
      
7. Register the render function using:

    * register(render);

8. Define your macro in a Markdown file.


##Callin the Macro in a Markdown File

To call a macro in a Markdown file, you use the following format:

    <div class="macro macro_macroname">
        Macro body code goes here.
    </div>

Where `macroname` is the name of your macro. So for example if we want to add the Google Maps macro, since it does not contain a body, we use:

    <div class="macro macro_googlemaps"></div>

For another example, take a look at the [code highlighting][] macro which takes the code itself as a body.

  [code highlighting]: /sampleapp/#/alkiradocs/MacroCode
