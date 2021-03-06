@metadata title=How to Create Macros
@metadata order=20
@metadata tagstring=macro alkira create new howto

[generic]: #/alkiradocs/MacroGeneric
[tasklet]: #/Overview/Tasklets
[alkira]: #/alkiradocs/Home
[code highlighting]: #/alkiradocs/MacroCode
[dashboard]: #/alkiradocs/MacroDashboard
[Sammy]: http://sammyjs.org/

#How to Create Macros
Adding dynamic content to an Alkira page is easy by using macros. There are two ways to add dynamic content:

1. using PyLabs tasklets
2. using JavaScript macros

Both options are explained in this section.


##PyLabs Tasklets
Creating PyLabs macros is creating a directory in `/opt/qbase5/lib/python/site-packages/alkira/tasklets/pylabsmacro` and putting one or more [tasklets][tasklet] in it.
Once you have created the directory with a tasklet, you can start using the macro by using the directory name.

For example, create a directory `demo` in `/opt/qbase5/lib/python/site-packages/alkira/tasklets/pylabsmacro` and create a tasklet in it.

In your Alkira page you can then use the macro \[\[demo\]\].

If you have more than one tasklet in the directory you must create a `match` function in the tasklets and provide a label or tags to the macro.
See the [generic] macro page for an example.


##JavaScript Macros
Instead of using PyLabs' macro system, you can also create your own macros in JavaScript. Below we elaborate how you can create a JavaScript macro by using the Google Maps macro as a reference.


###Google Maps Macro Code
Below you can find an example of a macro that shows a static Google map.


[[code]]
	//@metadata wizard=googlemaps
	//@metadata description=Shows Google Maps static map of choice
	//@metadata image=img/macros/googlemaps.png
	//@metadata documentationUrl=http://www.pylabs.org/#/alkiradocs/MacroGoogleMaps

    var render = function(options) {
        var $this = $(this);
            //define params that user can provide when adding the macro to a page
            var lat = parseFloat(options.params.latitude) || 51.1;
            var longitude = parseFloat(options.params.longitude) || 3.83333;
            var width = parseFloat(options.params.width) || 250;
            var height = parseFloat(options.params.height) || 250;
            var zoom = parseFloat(options.params.zoom) || 8;

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
[[/code]]

###Creating a Macro

1. Create a macro file under `/opt/qbase5/www/lfw/js/macros/`, for example `macrotest.js`.

    __Note:__ `lfw` is the acronym for _Lightning Fast Wiki_, which is the Incubaid code name for the [Alkira][] project.
    
2. Set the metadata for your macro. This information is used in the widget store when adding a widget to a [Dashboard][dashboard].
	* __//@metadata wizard__: name of the wizard that is launched when selecting the widget.
	* __//@metadata description__: description of the widget.
	* __//@metadata image__: link to image that is used in the widget store. The images must be stored in `/opt/qbase5/www/lfw/img/macros`, the link is relative from `/opt/qbase5/www/lfw/`.
	* __//@metadata documentationUrl__: link to the full documentation of the widget on www.pylabs.org

3. Define the parameters if any. You can set a default value for each parameter. In the example these parameters are defined with `options.params`, for example `var longitude = parseFloat(options.params.longitude);`.
You can provide default values by adding double pipe characters: `var longitude = parseFloat(options.params.longitude) || 3.83333;`

4. There must be a render function which takes `options` as a parameter. Options is an object with some parameters that we can use, such as:
    * __options.space__: get space name.
    * __options.page__: get page name.
    * __options.body__: get the page contents.
    * __options.tags__: get the tags of a page.
    * __options.params__: get the parameters that are passed to the macro tag, for example [[note:param1=value1]].
    * __options.query__: retrieves the query from a URL, for example the query `?space=myspace&page=mypage` results in `options.query.space=myspace` and `options.query.page=mypage`.
    * __options.pagecontent__: get the content of a page in HTML code.
    * __options.app__: get an instance of the '[Sammy][]' framework, which allows you to trigger actions.
    * __options.config__: get the configuration of the macro.
    * __options.saveConfig()__: saves the provided configuration of the macro.
    * __options.addCss()__: select a CSS style sheet either through a CSS file or a direct style code.
    * __options.addDependency()__: add a JavaScript library dependency if needed by the macro.
    * __options.swap()__: swap the old content of a page with new content.
    * __options.renderWiki()__: return the HTML element of a given Markdown syntax.

5. If you want to apply a special style sheet for your macro, you need the `options.addCss()` function. This function has three arguments:
    * __id:__ a unique id for your macro (usually just the macro name since it should be unique).
    * __tag:__ either "style" or "link" tag, where:

        * *style:* is used if you're giving it CSS dumped syntax.
        * *link:* is used if you're giving it a CSS file to load.

    * __params:__

        * if the tag is style, params is a dumped CSS string (as shown in the example).
        * if the tag is link, params is a key/value object.

        For example: 'params': {'rel': 'stylesheet', 'href': 'http://yandex.st/highlightjs/5.16/styles/default.min.css'}

6. You can load extra JavaScript libraries in your macro with the `options.addDependency` function. This functions requires two arguments:

    * __callback:__  callback function to be called after loading all dependency scripts, `cb` in the given example
    * __dependencies:__ list of file links to be loaded.

    In this case, you have to put all code that depends on the loaded dependencies in a callback function which you give as first argument to the `addDependency` function call.

7. Create a template using jQuery; jQuery.template(name, template) where:

    * __name:__ A string naming the compiled template.
    * __template:__ The HTML markup and/or text to be used as template. Can be a string, or an HTML element (or jQuery object wrapping an element) whose content is to be used as a template.

8. Render the specified HTML content as a template, using the specified data:

    jQuery.tmpl(name, [ options ]) where:

    * __name:__ A string naming the compiled template.
    * __options:__ An optional map of user-defined key-value pairs. Extends the tmplItem data structure, available to the template during rendering.

9. Register the render function using:

    * register(render);

10. Define your macro in a Markdown file.


###Calling the Macro in a Markdown File

To call a macro in a Markdown file, you use the following format:

    [[<macroname>]]
        Macro body code goes here.
    [[/<macroname>]]

Where `macroname` is the name of your macro, i.e. the name of the JavaScript file. For example if we want to add the Google Maps macro, since it does not contain a body, we use:

    [[googlemaps]][[/googlemaps]]

For another example, take a look at the [code highlighting][] macro which takes the code itself as a body.