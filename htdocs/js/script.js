/* Locations
 * =========
 * #/
 * --
 * Doesn't exits
 *
 * #/space
 * -------
 * Perform search request on GET when 'q' and 'type' query arguments are
 * provided.
 * Redirect to DEFAULT_PAGE_NAME otherwise.
 *
 * #/space/page
 * ------------
 * Display page content on GET
 */

(function($) {

var DEFAULT_PAGE_NAME = 'Home',
    LABELS_RE = /,\s*/,
    LOCATION_PREFIX = '#/';

var LFW = {};
LFW.macros = {};

var Utils = {
    removeYUICompressorMarks: function(text) {
        return text
            .replace(/\/\*!? YUI Compressor fix\s*/, '')
            .replace(/\s*YUI Compressor fix \*\/\s*/, '');
    },
    getTemplate: function(selector) {
        return Utils.removeYUICompressorMarks(
            $(selector).html());
    }
};

var app = $.sammy(function(app) {
    this.use('Title');
    this.use('Mustache');

    var _appName = null;
    var _space = null,
        _page = null;
    var csses = new Array();
	var cssLoaded = false;

    var swap = function(html, base, root) {

        base = base || ''; // location #/space/page
        root = root || null;

        console.log('SWAP START: base ' + base + 'root ' + root);

        console.log('SWAP content: ' + html);

        var elem = $('<div>' + html + '</div>');

        if (root === null) {
          $('#main')
            .empty()
            .append(elem);
        } else {
          $(root)
            .empty()
            .append(elem);
        }


        // Replace anchor links
        $('#main a[href]')
            .filter(function() {
                return ($(this).attr('href') || ' ')[0] === '#';
            })
            .each(function() {
                $this = $(this);

                var loc = base + '/' + $this.attr('href');

                $this.attr('href', loc);
            });

        console.log('SWAP END: base ' + base);


        $('.macro', elem).each(function() {
            var $this = $(this),
                classes = ($this.attr('class') || '').split(/\s+/),
                name = null,
                context = this,
                data = $this.html(),
                params = $.parseJSON(htmlDecode($this.attr('params'))) || new Object();

            $this.empty();

            for(var i = 0, len = classes.length; i < len; i++) {
                var class_ = classes[i];

                if(class_.match(/^macro_/)) {
                    if(name != null) {
                        throw new Error('Multiple macro names found');
                    }

                    name = class_.replace(/^macro_/, '');
                }
            }

            var render = function() {

                var options = {
                    'space': getSpace(),
                    'page': getPage(),
                    'body': data,
                    'params': params,
                    'pagecontent': elem,
                    'addDependency': addDependency,
                    'addCss': function(cssobject) {
                    	addCss(cssobject);
                    },
                    'swap': function(html) {
                    	swap(html, base, $this);
                    },
                    'renderWiki': function(mdstring) {
                    	return renderWiki(mdstring);
                    }
                };
                console.log('Start rendering macro ' + name + ' - ' + data);
                try{
                    LFW.macros[name].call(context, options);
                }catch(err){
                    $this.append("<div class='macro_error'>Macro "+ name +" failed to render<br>"+err+"</div>")
                }
                console.log('Stop rendering macro ' + name + ' - ' + data);
            };

            if(!LFW.macros[name]) {
                LFW.macros[name] = [render];

                // Load macro
                console.log('Loading macro ' + name);

                var jqxhr = $.get(LFW_CONFIG['uris']['macros'] + name + '.js',
                    function(data, textStatus, jqXHR) {

                    var script = '' +
'var __exec_context_321 = this,\n' +
'    register = function(render) {\n' +
'        __exec_context_321.macros[\'' + name + '\'] = render;\n' +
'    };\n' +
'\n' +
data;

                    var fun = new Function(script),
                        ctx = {};

                    ctx.macros = {};
                    fun.call(ctx);

                    if(!$.isFunction(ctx.macros[name])) {
                        throw new Error('Macro not registered');
                    }

                    var waiting = LFW.macros[name];

                    LFW.macros[name] = ctx.macros[name];

                    for(var i = 0, len = waiting.length; i < len; i++) {
                        waiting[i]();
                    }
                },
                    'text'
                )
                .success()
                .error(function(data, textStatus, jqXHR) {
                    console.log('Failed to load Macro: ' + textStatus);
                })
                .complete();
            }
            else {
                if(!$.isFunction(LFW.macros[name])) {
                    LFW.macros[name].push(render);
                }
                else {
                    render();
                }
            }
        });



    };

    var buildUri = function(space, page) {
        if(!space) {
            return LOCATION_PREFIX;
        }
        else if(!page) {
            return LOCATION_PREFIX + space;
        }
        else {
            return LOCATION_PREFIX + space + '/' + page;
        }
    };

    var setSpace = function(space) {
        _space = space;

        var spaces = $('#space option');
        for(var i = 0; i < spaces.length; i++) {
            if(spaces[i].value === space) {
                $(spaces[i]).attr('selected', '1');
            }
        }

        $('form#label-search').attr('action', buildUri(space));
        $('form#fulltext-search').attr('action', buildUri(space));

        var completionUri = LFW_CONFIG['uris']['completion'];

        $('#title').autocomplete('option', 'source',
            function(request, response) {
                var term = request.term,
                    completionUri = LFW_CONFIG['uris']['title'];

                $.getJSON(completionUri, {
                    'space': space,
                    //'type': 'title',
                    //'q': term
                    'term': term
                }, response);
            }
        );

        $('#labels').autocomplete('option', 'source',
            function(request, response) {
                var term = request.term.split(LABELS_RE).pop(),
                    completionUri = LFW_CONFIG['uris']['tags'];

                $.getJSON(completionUri, {
                    // 'space': space,
                    //'type': 'labels',
                    //'q': term
                    'term': term
                }, response);
            }
        );
    };
    var getAppName = function () {
        if( ! _appName ) {
            _appName = LFW_CONFIG['appname'];
            if( _appName == '' ) {
                throw new Error( 'Appname is an emtpy string' )
            }
            if( ! _appName  ) {
                throw new Error( 'Appname is null' )
            }
        }
        return _appName;
    }
    var getSpace = function() {
        if(!_space) {
            throw new Error('Space requested whilst it\'s not set');
        }

        return _space;
    };

    var setPage = function(page) {
        _page = page;
    },
        getPage = function() {
        return _page;
    }
    
    var htmlEncode = function(value){
        if (!value){
            return '';
        }
        return $('<div/>').text(value).html();
    }

    var htmlDecode = function(value){
        if (!value){
            return '';
        }
        return $('<div/>').html(value).text();
    }

    var renderWiki = function(mdstring) {
        mdstring = mdstring || '';
        mdstring = mdstring.replace(/\n?(..)?\[\[(\w+)(:[^\]]+)?\]\]([.\s\S]*?[\s\S])??(\[\[\/\2\]\])/g ,
            function(fullmatch, _, macroname, paramstring, body, m3){
                if (fullmatch.substr(0, 2) == "  "){
                    return fullmatch;
                }
                var result = '\n<div class="macro macro_' + macroname + '"'
                if (paramstring){
                    paramstring = paramstring.substr(1);
                    var params = new Object();
                    $.each(paramstring.split(","), function(idx, param){
                        if ( param.search("=") != -1){
                            var keyvalue = param.split("=");
                            params[keyvalue[0].trim()] = keyvalue[1].trim();
                        }
                    });
                    result += " params='" + htmlEncode($.toJSON(params)) + "'";
                }
                body = body || '';
                result += ">" + body.trim() + "\n</div>"
                return result;
            });
        var compiler = new Showdown.converter();
        var result = compiler.makeHtml(mdstring);
        return result;
    }

	function inArray(element, array) {
		for (index in array) {
			if (array[index] == element) {
				return true;
			}
		}
		return false;
	}

    var addDependency = function(callback, dependencies, ordered) {

        var seperator = ordered == undefined ? " " : ">";
    	console.log('in adddependency');
        var depstring = "";
        $.each(dependencies, function(idx, script){
            depstring += script + " " + seperator + " ";
        });
        if (depstring !== ""){
            depstring = depstring.substring(0, depstring.length - 3);
        }
        dominoes(depstring, callback);
    }

    function loadCss() {
    	csslinks = $('link');
    	$.each(csslinks, function(index, csslink) {
    		id = csslink.id;
    		if (id != undefined) addCssId(id);
    	});
    	cssStyles = $('style');
    	$.each(cssStyles, function(index, cssStyle) {
    		id = cssStyle.id;
    		if (id != undefined) addCssId(id);
    	})
    	cssLoaded = true;
    };

	var addCssId = function(id) {
		console.log('adding cdd with id: ' + id);
		if (!inArray(id, csses)) {
			csses.push(id);
			return true;
		}
		return false;
	};

	var addCss = function(cssobject) {
		console.log('in addCss');
    	if (cssLoaded == false) {
    		loadCss();
    	}
    	id = cssobject['id'];
    	if (addCssId(id) == true) {
    		tagname = cssobject['tag'];
    		params = cssobject['params'];
			var head = document.getElementsByTagName("head")[0] || document.documentElement;
			var cssNode = document.createElement(tagname);
			cssNode.id = id;

    		if (tagname == 'link'){
				//To add a css link i.e. <link rel="stylesheet" href="mystyle.css">
				cssNode.type = params['type'] || 'text/css';
				cssNode.rel = params['rel'];
				cssNode.href = params['href'];
    		}
    		else {
    			// To add a css style i.e.   <style type="text/css">
    										//html { height: 100% }
    										//body { height: 100%; margin: 0px; padding: 0px }
    										//#map_canvas { height: 100% }
  											//</style>
				cssNode.innerHTML += params;
    		}
    		head.insertBefore( cssNode, head.firstChild );
    	}
    }

    this.setTitle(function(title) {
        return [title, getSpace(), 'LFW'].join(' / ');
    });

    var clearFields = function() {
        var fields = ['title', 'labels', 'text'];

        for(var i = 0; i < fields.length; i++) {
            $('#' + fields[i]).val('').blur();
        }
    };

    this.get('#/:space', function() {
        setSpace(this.params['space']);
        setPage(null);

        clearFields();

        var context = this;

        if(this.params['q'] && this.params['type']) {
            // This is a search request
            var type = this.params['type'],
                query = this.params['q'],

                searchUri = LFW_CONFIG['uris']['search'];

           if(type === 'labels') {
               query = $(query.split(LABELS_RE)).map(function(_, s) {
                   return s.replace(/\+/g, ' ').trim();
               });
           }

           var args = {
               space: getSpace()
           };

           if(type === 'labels') {
               args['tags'] = this.params['q'];
           }
           else if(type === 'fulltext') {
               args['text'] = this.params['q'];
           }
           else {
               throw new Error('Invalid query type');
           }

           $.getJSON(searchUri, /*{
               'type': type,
               'space': getSpace(),
               'q': query
           },*/
           args,
           function(data) {
               context.title('Search Results');

               var templateData = [];
               for(var i = 0, len = data.length; i < len; i++) {
                   var result = data[i];
                   var appName = getAppName();
                   templateData.push([result.space, result.name, appName]);
               }

               swap(
                   context.mustache(
                       Utils.getTemplate('#search-result-template'),
                       {'results': templateData}
                   )
               );
           });

        }
        else {
            this.trigger('change-page', {'title': DEFAULT_PAGE_NAME});
        }
    });

    this.get('#/:space/:page', function() {

        clearFields();

        var space = this.params['space'],
            page = this.params['page'];

        var render = true;

        if (page.substr(-3) === '.md') {
            page = page.substr(0, page.length - 3);
            render = false;
        }

            //pageUri = LFW_CONFIG['uris']['pages'] + '/' + space + '/' + page;
        var pageUri = LFW_CONFIG['uris']['pages'] + '?space=' + space +
                '&name=' + page;

        setSpace(space);
        setPage(page);

        var context = this;

        $.ajax({
            url: pageUri,
            success: function(data) {
                context.title(page);

                var content = data['content'];

                if(!content || !content.length || content.length === 0) {
                    context.notFound();
                    return;
                }

                console.log('Page source: ' + content);
                if(render === true) {
                    rendered = renderWiki(content);
                } else {

                    rendered = $('<div><pre>' + content + '</pre></div>').html();
                    //rendered.append($('<div/>').text(content).text());

                    //rendered = rendered.html();
                }
                console.log('Page rendered: ' + rendered);

                swap(rendered, '#/' + space + '/' + page);
            },
            //cache: false,
            dataType: 'json',
            error: function(xhr, text, exc) {
                if(xhr.status === 404) {
                    context.notFound();
                }
                else {
                    app.error('Unknown error: ' + text, exc);
                }
            }
        });
    });

    this.get('#/:space/:page/#:anchor', function() {
        var target_offset = $('#' + this.params['anchor']).offset(),
            target_top = target_offset.top;

        $('html, body').animate({
            scrollTop: target_top
        }, 500);

    });

    /**
     * Pylabs Wizards integration
     **/
    this.post('#/action/:action', function () {
       alert('Hello, executing action  ' + this.params['action']);
       return false;
    });



    this.bind('change-space', function(e, data) {
        this.log('change-space');
        setSpace(data['space']);
        this.trigger('change-page', {'title': DEFAULT_PAGE_NAME});
    });

    this.bind('error', function(e, data) {
        var error_template = Utils.getTemplate('#error-template');

        this.title('Error');
        swap(this.mustache(error_template, data));
    });

    this.bind('change-page', function(e, data) {
        this.log('change-page');
        this.redirect(buildUri(getSpace(), data['title']));
    });
});

$(function() {
    if(typeof(LFW_CONFIG) === 'undefined' || !LFW_CONFIG) {
        throw new Error('No LFW_CONFIG defined');
    }

    // Set up spaces dropdown
    $.getJSON(LFW_CONFIG['uris']['listSpaces'], function(data) {
        var spaces = $('#space');
            for(var i = 0; i < data.length; i++) {
                $('<option>')
                    .attr('value', data[i])
                    .text(data[i])
                    .appendTo(spaces);
            }

            spaces.change(function() {
                app.trigger('change-space', {space: $(this).val()});
            });

            app.run('#/' + $('#space').val() + '/' + DEFAULT_PAGE_NAME);
    });

    // Set up search boxes
    $('#labels')
        .bind('keydown', function(event) {
            if(event.keyCode === $.ui.keyCode.TAB &&
                $(this).data('autocomplete').menu.active) {
                event.preventDefault();
            }

            if(event.keyCode === $.ui.keyCode.ENTER &&
                !$(this).data('autocomplete').menu.active) {
                event.preventDefault();

                if(this.value && this.value !== '') {
                    $('form#label-search').submit();
                }

                return false;
            }

            return true;
        })
        .autocomplete({
            minLength: 0,
            source: [],
            focus: function() {
                return false;
            },
            select: function(event, ui) {
                var terms = this.value.split(LABELS_RE);
                terms.pop();
                terms.push(ui.item.value);
                terms.push('');
                this.value = terms.join(', ');
                return false;
            }
        });

    $('#title')
        .bind('keydown', function(event) {
            if(event.keyCode != $.ui.keyCode.ENTER ||
                $(this).data('autocomplete').menu.active) {
                return true;
            }

            event.preventDefault();

            var title = this.value;

            if(!title || title === '') {
                app.log('No title provided');
            }
            else {
                app.trigger('change-page', {'title': title});
            }

            return false;
        })
        .autocomplete({
            source: []
        });

    $('#spinner')
        .ajaxStart(function() {
            $(this).show();
        })
        .ajaxStop(function() {
            $(this).hide();
        })
        .hide();
});

})(this.jQuery);

// vim: tabstop=4:shiftwidth=4:expandtab
