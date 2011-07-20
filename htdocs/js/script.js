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
    LOCATION_PREFIX = '#/',
    ADMINSPACE="Admin";

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

$.fillSpacesList = function(options) {
    var options = $.extend({success: $.noop}, options);

    $.getJSON(LFW_CONFIG['uris']['listSpaces'], function(data) {
        var spaces = $('#space');
        spaces.empty();
        for(var i = 0; i < data.length; i++) {
            if (Auth.getFromLocalStorage("username") == null && data[i] == ADMINSPACE) {
                continue;
            }
            $('<option>')
                .attr('value', data[i])
                .text(data[i])
                .appendTo(spaces);
        }

        options.success();
    });
};

var app = $.sammy(function(app) {
    this.use('Title');
    this.use('Mustache');

    var _appName = null;
    var _space = null,
        _page = null,
        _query = null;
    var csses = new Array();
    var cssLoaded = false;
    var _pageobj = null;

    var swap = function(html, base, root, addItem, macroElem) {

        base = base || ''; // location #/space/page
        root = root || null;

        console.log('SWAP START: base ' + base + 'root ' + root);

        console.log('SWAP content: ' + html);

        var elem;
        if (!addItem && !macroElem) {
            elem = $('<div>' + html + '</div>');
        } else {
            elem = $(html);
        }

        if (root === null) {
          $('#main')
            .empty()
            .append(elem);
        } else {
            if (!addItem) {
                $(root).empty().append(elem);
            } else {
                $(root).append(elem);
            }
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


        $('.macro', (macroElem ? macroElem : elem)).each(function() {
            var $this = $(this),
                classes = ($this.attr('class') || '').split(/\s+/),
                name = null,
                context = this,
                macroname = null,
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

            macroname = name;

            var render = function() {

                var options = {
                    'space': getSpace(),
                    'page': getPage(),
                    'body': htmlDecode(data),
                    'params': params,
                    'query': getQuery(),
                    'pagecontent': elem,
                    'config': {},

                    'addDependency': function(callback, dependencies, ordered){
                        addDependency(callback, dependencies, ordered, $this, name);
                    },
                    'addCss': function(cssobject) {
                        addCss(cssobject);
                    },
                    'swap': function(html, customRoot, addItem, customMacroElem) {
                        // Make sure our customRoot is something from within our macro
                        swap(html, base, (customRoot && $this.has(customRoot) ? customRoot : $this), addItem,
                            customMacroElem);
                    },
                    'renderWiki': function(mdstring) {
                        return renderWiki(mdstring);
                    },
                    'saveConfig': function() {
                        saveConfig(options.config, name, params.config);
                    }
                };

                // Keep track of how many ajax calls we need to do before we can render our macro
                var ajaxTodo = 0;
                if (params.config) {
                    ++ajaxTodo;
                }
                if (typeof(params.call) === 'string') {
                    ++ajaxTodo;
                }

                var renderMacro = function() {
                    --ajaxTodo;
                    if (ajaxTodo > 0) {
                        console.log('Waiting for ' + ajaxTodo + ' more ajax calls before rendering macro ' + name);
                        return;
                    }
                    console.log('Start rendering macro ' + name + ' - ' + data);
                    try{
                        options.params.macroname = name;
                        LFW.macros[name].call(context, options);
                    }catch(err){
                        $this.append("<div class='macro_error'>Macro "+ name +" failed to render<br>"+err+"</div>");
                    }
                    console.log('Stop rendering macro ' + name + ' - ' + data);
                };

                if (typeof(params.call) === 'string') {
                    // Call the url
                    console.log('Calling data from ' + params.call + ' for macro ' + name);
                    $.ajax({
                        url: params.call,
                        dataType: 'text',
                        success: function(data) {
                            console.log('Got the data for macro ' + name + ' from ' + params.call);
                            options.body = data;
                            renderMacro();
                        },
                        error: function() {
                            console.log('Error loading macro data for ' + name + ' from ' + params.call);
                            if (options.body.trim().length) {
                                // We have a default body, so pass that
                                console.log('Loading macro ' + name + ' with default data ' + options.body);
                                renderMacro();
                            } else {
                                // Show error
                                options.swap('Error loading ' + params.call + ' for macro ' + name);
                            }
                        }
                    });
                }
                if (params.config) {
                    // Get the config if any
                    console.log('Getting config for macro ' + name);
                    var configData = { space: getSpace(), page: getPage(), macro: macroname };
                    if (typeof(params.config) === "string" && params.config.toLowerCase() !== "true") {
                        configData.configId = params.config;
                    }
                    $.ajax({
                        url: LFW_CONFIG.uris.macroConfig,
                        dataType: 'json',
                        data: configData,
                        success: function(data) {
                            console.log('Got config for macro ' + name + ' : ' + data);
                            options.config = data;
                            renderMacro();
                        },
                        error: function() {
                            console.log('Error getting config for macro ' + name);
                            renderMacro();
                        }
                    });
                }
                if (!ajaxTodo) {
                    renderMacro();
                }
            };

            if(!LFW.macros[name]) {
                LFW.macros[name] = [render];

                // Load macro
                console.log('Loading macro ' + name);

                var loadmacroscript = function() { $.get(LFW_CONFIG['uris']['macros'] + macroname + '.js',
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
                    if (name != 'generic') {
                        macroname = 'generic';
                        loadmacroscript();
                        return;
                    }
                    console.log('Failed to load Macro: ' + textStatus);
                })
                .complete();
                };
                loadmacroscript();
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

    var setSpace = function(space, force) {
        if (space == _space && !force)
            return;

        _space = space;
        if (space == ADMINSPACE){
            $("#toolbar").css("visibility", "hidden");
        } else {
            $("#toolbar").css("visibility", "visible");
        }

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
                    'space': space,
                    //'type': 'labels',
                    //'q': term
                    'term': term
                }, response);
            }
        );

        var pageTreeUri = LFW_CONFIG['uris']['pages'] + '?space=' + space +
                '&name=' + 'pagetree';

        var context = this;
        var treePage = '#/' + space + '/pagetree';
        
        var toggleSidebar = function(visible) {
            if (visible){
                $("#sidebar").show(0);
                $("#content").addClass("span-19");
                $("#toolbar").addClass("span-20");
                $("#main").addClass("span-20");
            } else {
                $("#sidebar").hide(0);
                $("#content").removeClass("span-19");
                $("#toolbar").removeClass("span-20");
                $("#main").removeClass("span-20");
            }
        };
        $.ajax({
            url: pageTreeUri,
            success: function(data) {
                var content = data['content'];
                if(!content || !content.length || content.length === 0) {
                    content = "";
                }

                console.log('Tree source: ' + content);
                rendered = renderWiki(content);
                console.log('Tree rendered: ' + rendered);
                if (rendered !== ""){
                    toggleSidebar(true);
                } else {
                    toggleSidebar(false);
                }
                swap(rendered, treePage, '#tree');
            },
            //cache: false,
            dataType: 'json',
            error: function(xhr, text, exc) {
                toggleSidebar(false);
                swap("", treePage, '#tree');
            }
        });
    };
    var getAppName = function () {
        if( ! _appName ) {
            _appName = LFW_CONFIG['appname'];
            if( _appName == '' ) {
                throw new Error( 'Appname is an emtpy string' );
            }
            if( ! _appName  ) {
                throw new Error( 'Appname is null' );
            }
        }
        return _appName;
    };
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
    };
    var setQuery = function(query) {
        _query = query;
    };

    var getQuery = function(){
        return _query;
    };

    var setPageObj = function(page){
        _pageobj = page;
    };

    var setTitle = function(title) {
        _title = title;
    };

    var getTitle = function(){
        return _title;
    };

    this.getPage = getPage;
    this.getTitle = getTitle;
    this.getSpace = getSpace;
    this.setSpace = setSpace;

    this.getPageObj = function(){
        return _pageobj;
    };

    var htmlEncode = function(value){
        if (!value){
            return '';
        }
        return $('<div/>').text(value).html();
    };

    var htmlDecode = function(value){
        if (!value){
            return '';
        }
        return $('<div/>').html(value).text();
    };

    var renderWiki = function(mdstring) {
        mdstring = mdstring || '';
        var regex = /\n?(..)?\[\[(\w+)(:[^\]]+)?\]\]([.\s\S]*?[\s\S])??(\[\[\/\2\]\])/g;
        var regex2 = /\n?(..)?\[\[(\w+)(:[^\]]+)?\/\]\]/g;
        var replacefunc = function(fullmatch, macroname, paramstring, body){
            if (fullmatch.substr(0, 2) == "  "){
                return fullmatch;
            }
            var result = '\n<div class="macro macro_' + macroname + '"';
            if (paramstring){
                paramstring = paramstring.substr(1);
                paramstring = "," + paramstring;
                var params = new Object();
                var pieces = paramstring.split(/,\s*(\w+)\s*=\s*/);
                for (var i = 1; i < pieces.length; i+=2)
                {
                    var key = pieces[i];
                    var param = pieces[i+1];
                    params[key] = param;
                }
                result += " params='" + htmlEncode($.toJSON(params)) + "'";
            }
            body = body || '';
            result += ">" + htmlEncode(body.trim()) + "\n</div>";
            return result;
        };

        mdstring = mdstring.replace(regex ,
            function(fullmatch, _, macroname, paramstring, body, _){
                return replacefunc(fullmatch, macroname, paramstring, body);
            });
        mdstring = mdstring.replace(regex2 ,
            function(fullmatch, _, macroname, paramstring){
                return replacefunc(fullmatch, macroname, paramstring, null);
            });

        // Allow anchors to space and page
        // These regexes are taking from the Showdown source
        // See https://github.com/coreyti/showdown/blob/master/src/showdown.js for more information
        // Specifically function _StripLinkDefinitions and _DoAnchors
        var simpleAnchorRegex = /(\[((?:\[[^\]]*\]|[^\[\]])*)\]\([ \t]*()<?(.*?)>?[ \t]*((['"])(.*?)\6[ \t]*)?\))/g;
        var linkDefinitionsRegex = /^[ ]{0,3}\[(.+)\]:[ \t]*\n?[ \t]*<?(\S+?)>?[ \t]*\n?[ \t]*(?:(\n*)["(](.+?)[")][ \t]*)?(?:\n+|\Z)/gm;
        var replaceLink = function(url) {
            if (!url.length) {
                return url;
            }
            if (url.indexOf("#/") === 0) {
                // Match for "#/space/page" links
                return "/" + getAppName() + "/" + url;
            } else if (url.indexOf(":") === -1 && url.indexOf("#") !== 0 && url.indexOf("/") === -1) {
                // Match for "page" links, all external links in markdown need : to work afaik
                // We ignore # as well if we're linking to an anchor
                // Anything containing a / is ignore as well
                return "/" + getAppName() + "/#/" + getSpace() + "/" + url;
            }
            return url;
        };

        mdstring = mdstring.replace(simpleAnchorRegex, function(fullMatch, m1, m2, m3, url, title) {
            title = (title ? title : "")
            return fullMatch.replace(new RegExp("\\(\\s*" + url + "\\s*" + title + "\\s*\\)"),
                "(" + replaceLink(url) + " " + title + ")");
        });
        mdstring = mdstring.replace(linkDefinitionsRegex, function(fullMatch, m1, url) {
            return fullMatch.replace(url, replaceLink(url));
        });

        var compiler = new Showdown.converter();
        var result = compiler.makeHtml(mdstring);
        return result;
    };

    function inArray(element, array) {
        for (index in array) {
            if (array[index] == element) {
                return true;
            }
        }
        return false;
    }

    var addDependency = function(callback, dependencies, ordered, element, name) {

        var seperator = ordered == undefined ? " " : ">";
        console.log('in adddependency');
        var depstring = "";
        $.each(dependencies, function(idx, script){
            depstring += script + " " + seperator + " ";
        });
        if (depstring !== ""){
            depstring = depstring.substring(0, depstring.length - 3);
        }
        dominoes(depstring, function(){
            try{
                callback();
            }catch(err){
                element.append("<div class='macro_error'>Macro "+ name +" failed <br/>"+err+"</div>");
            }
        });
    };

    function loadCss() {
        var csslinks = $('link');
        $.each(csslinks, function(index, csslink) {
            id = csslink.id;
            if (id != undefined) addCssId(id);
        });
        var cssStyles = $('style');
        $.each(cssStyles, function(index, cssStyle) {
            id = cssStyle.id;
            if (id != undefined) addCssId(id);
        });
        cssLoaded = true;
    }

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
        var id = cssobject['id'];
        if (addCssId(id) == true) {
            var tagname = cssobject['tag'];
            var params = cssobject['params'];
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
    };

    var saveConfig = function(config, macroname, configid) {
        console.log('Saving config for macro ' + macroname + ' : ' + config);
        // No clue why but we need a double JSON.stringify here for things to work
        var data = { space: getSpace(), page: getPage(), macro: macroname, config: JSON.stringify(JSON.stringify(config)) };
        if (typeof(configid) === "string" && configid.toLowerCase() !== "true") {
            data.configId = configid;
        }
        $.ajax({
            url: LFW_CONFIG.uris.updateMacroConfig,
            dataType: "text",
            data: data,
            type: "POST",
            success: function(data) {
                console.log('Saving of config successful for macro ' + macroname);
            },
            error: function() {
                console.log('Error saving config for macro ' + macroname);
            }
        });
    };

    this.setTitle(function(title) {
        return [title, getSpace()].join(' - ');
    });

    var clearFields = function() {
        var fields = ['title', 'labels', 'text'];

        for(var i = 0; i < fields.length; i++) {
            $('#' + fields[i]).val('').blur();
        }
    };

    // Check wether a token parameter was added to the url, if so use this as an OAuth token
    var checkToken = function() {
        if (this.params.hasOwnProperty("token") && Auth.parseOAuthToken) {
            Auth.parseOAuthToken(this.params.token, (this.params.user ? this.params.user : ""), true);

            // We only want to do this once
            delete this.params.token;
            delete this.params.user;
        }
    };

    this.get('#/:space', function() {
        checkToken.call(this);

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
               //space: getSpace()
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
        checkToken.call(this);

        clearFields();

        var space = this.params['space'],
            page = this.params['page'];

        var render = true;

        //pages with /'s should be left unchanged
        if (page.substr(-3) === '.md') {
            if (page.indexOf("/") < 0)
                page = page.substr(0, page.length - 3);
            render = false;
        }

            //pageUri = LFW_CONFIG['uris']['pages'] + '/' + space + '/' + page;
        var pageUri = LFW_CONFIG['uris']['pages'] + '?space=' + space +
                '&name=' + page;

        setSpace(space);
        setPage(page);
        setQuery(this.params);



        var context = this;

        $.ajax({
            url: pageUri,
            success: function(data) {
                setPageObj(data);
                if (data['code']) {
                    $("#toolbar > button").button("option", "disabled", true);
                    if (data['code'] == 404)
                    {
                        data = {title: 'Page Not Found',
                                pagetype: 'md',
                                content: '## Page Not Found\n\
\n\
###To create new page\n\
\n\
- Navigate to the place where you want to place page\n\
- Press the _New_ button\n\
- Enter page *Name* and *Title* and write the page content\n\
- Press Save\n'};
                        //context.notFound();
                    } else {
                        app.error('Unknown error: ' + data['error']);
                        return;
                    }
                } else {
                    $("#toolbar > button").button("option", "disabled", false);
                }

                if (page == "Home") {
                    //disable deleting of Home page.
                    $("#toolbar > #deletepage").button("option", "disabled", true);
                }

                context.title(data['title']);

                var content = data['content'];

                setTitle(data['title']);

                if (data.pagetype != "md") {
                    content = '[[code]]\n' + content + '[[/code]]';
                }

                /*
                if(!content || !content.length || content.length === 0) {
                    context.notFound();
                    return;
                }
                */

                console.log('Page source: ' + content);
                if(render === true) {
                    rendered = renderWiki(content);
                } else {

                    rendered = $('<div><pre>' + content.replace(/</g, "&lt;") + '</pre></div>').html();
                    //rendered.append($('<div/>').text(content).text());

                    //rendered = rendered.html();
                }

                //For page name that contains /, display its path as header (appname/page.name)
                if (data.name && data.name.indexOf("/") > 0)
                    rendered = "<h4><br>" + LFW_CONFIG.appname + "/" + data.name + "</h4>" + rendered

                console.log('Page rendered: ' + rendered);

                swap(rendered, '#/' + space + '/' + page);
            },
            //cache: false,
            dataType: 'json',
            error: function(xhr, text, exc) {
                if (xhr.status === 404) {
                    context.notFound();
                } else if (xhr.status === 401) {
                    swap("<p class='error'> Invalid User Name /Password</p>", '#/' + space + '/' + page);
                } else if (xhr.status === 403) {
                    swap("<p class='error'>Authentication needed</p>", '#/' + space + '/' + page);
                } else if (xhr.responseText.indexOf("Authorization failed") > 0) {
                    swap("<p class='error'> Authorization failed</p>", '#/' + space + '/' + page);
                } else {
                    app.error('Unknown error: ' + text, new Error(exc));
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
        //replace /s with %2f
        data['title'] = data['title'].replace(/\//g, "%2f");
        this.redirect(buildUri(getSpace(), data['title']));
    });
});



$(function() {
    if(typeof(LFW_CONFIG) === 'undefined' || !LFW_CONFIG) {
        throw new Error('No LFW_CONFIG defined');
    }

    $("#space").change(function() {
        app.trigger('change-space', {space: $(this).val()});
    });

    // Set up spaces dropdown
    $.fillSpacesList({success: function(){
        app.run('#/' + $('#space').val() + '/' + DEFAULT_PAGE_NAME);
    }});

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

$(function(){
    //build editor buttons and dialog
    var dialog = $("<div>")
                .editor()
                .dialog({autoOpen: false,
                        modal: true,
                        width: '80%',
                        height: $(document).height() - 50,
                        title: "Page Editor",
                        closeOnEscape: false
                        });

    $("#toolbar > #newpage").button({icons: {primary: 'ui-icon-document'}}).click(function(){
        var parent = app.getPage();
        var space = app.getSpace();
        var defaultname = ''
        if (parent.indexOf("/") > 0)
        {
            idx = parent.lastIndexOf("/")
            defaultname = parent.substr(0, idx + 1) + 'untitled'
        }

        dialog.editor("name", defaultname);
        dialog.editor("title", "");
        dialog.editor("content", "");
        dialog.editor("filetype", "md");

        dialog.editor("disabled", "name", false);
        dialog.editor("disabled", "title", false);
        dialog.dialog("option", "buttons", {Close: function() {
                                                $dialog = $(this);
                                                if ("" != $dialog.editor("content")) {
                                                    $.confirm("There are some unsaved changes, are you sure you want to close the editor", {title: 'Unsaved Changes',
                                                        ok: function(){
                                                            $dialog.dialog("close");
                                                        }});
                                                } else {
                                                    $dialog.dialog("close");
                                                }
                                            },
                                            Save: function() {
                                                var saveurl = LFW_CONFIG['uris']['createPage'];
                                                var name = $.trim(dialog.editor("name"));
                                                var title = $.trim(dialog.editor("title"));
                                                var filetype = dialog.editor('filetype');

                                                if (!name) {
                                                    $.alert("Name can't be empty", "Invalid Name");
                                                    return;
                                                }
                                                if(!title){
                                                    title = name;
                                                }

                                                var content = dialog.editor("content");

                                                $.ajax({
                                                        url: saveurl,
                                                        type: 'POST',
                                                        data: {'space': space,
                                                               'name': name,
                                                               'pagetype': filetype,
                                                               'content': content,
                                                               'title': title,
                                                               'parent': parent},
                                                        dataType: 'json',
                                                        success: function(data) {
                                                            //triger sync
                                                            if (space == 'Imported') {
                                                                $.ajax({url: 'appserver/rest/ui/editor/exportFile',
                                                                        data: {'pagename': name},
                                                                        dataType: 'json',
                                                                        error: $.alerterror
                                                                        });
                                                            }
                                                            app.trigger('change-page', {title: name});
                                                            app.setSpace(space, true);
                                                            dialog.dialog("close");
                                                        },
                                                        error: $.alerterror
                                                    });
                                            }});
        dialog.dialog("open");
    });

    $("#toolbar > #editpage").button({icons: {primary: 'ui-icon-gear'}}).click(function(){
        var space = app.getSpace();
        var pageobj = app.getPageObj();
        var content = pageobj.content;

        dialog.editor("title", app.getTitle());
        dialog.editor("name", pageobj.name);
        if (pageobj.name === "Home"){
            dialog.editor("disabled", "name", true);
            dialog.editor("disabled", "title", true);
        } else {
            dialog.editor("disabled", "name", false);
            dialog.editor("disabled", "title", false);
        }
        dialog.editor("content", content === null ? "" : content);
        dialog.editor("filetype", pageobj.pagetype);
        dialog.dialog("option", "buttons", {Close: function() {
                                                $dialog = $(this);
                                                if (content != $dialog.editor("content")) {
                                                    $.confirm("There are some unsaved changes, are you sure you want to close the editor", {title: 'Unsaved Changes',
                                                        ok: function(){
                                                            $dialog.dialog("close");
                                                        }});
                                                } else {
                                                    $dialog.dialog("close");
                                                }
                                            },
                                            Save: function() {
                                                    var saveurl = LFW_CONFIG['uris']['updatePage'];

                                                    //append ext if needed.
                                                    var filetype = dialog.editor('filetype');
                                                    var name = $.trim(dialog.editor("name"));
                                                    var title = $.trim(dialog.editor("title"));
                                                    if (!name){
                                                        $.alert("Page name can't be empty", "Invalid Name");
                                                    }
                                                    if (!title){
                                                        title = name;
                                                    }

                                                    $.ajax({url: saveurl,
                                                            type: 'POST',
                                                            data: {'space': space,
                                                                   'name': pageobj.name,
                                                                   'newname': name,
                                                                   'pagetype': filetype,
                                                                   'content': dialog.editor("content"),
                                                                   'title': title},
                                                            dataType: 'json',
                                                            success: function(data) {
                                                                //triger sync
                                                                if (space == 'Imported') {
                                                                    $.ajax({url: 'appserver/rest/ui/editor/exportFile',
                                                                            data: {'pagename': name,
                                                                                   'oldpagename': pageobj.name},
                                                                            dataType: 'json',
                                                                            error: $.alerterror
                                                                            });
                                                                }
                                                                app.trigger('change-page', {title: name});
                                                                dialog.dialog("close");
                                                            },
                                                            error: $.alerterror
                                                        });

                                                }});
        dialog.dialog("open");
    });

    $("#deletepage").button({icons: {primary: 'ui-icon-close'}}).click(function(){
        $.confirm("Are you sure you want to delete this page?", {title: "Delete Page",
            ok: function() {
                var deleteurl = LFW_CONFIG['uris']['deletePage'];
                var page = app.getPage();
                var space = app.getSpace();
                $.ajax({
                        url: deleteurl,
                        data: {'space': space,
                               'name': page},
                        dataType: 'json',
                        success: function(data) {
                            //triger sync
                            if (space == 'Imported') {
                                $.ajax({url: 'appserver/rest/ui/editor/deleteFile',
                                        data: {'pagename': page},
                                        dataType: 'json',
                                        error: $.alerterror
                                        });
                            }
                            app.trigger('change-page', {title: DEFAULT_PAGE_NAME});
                            app.setSpace(space, true);
                        },
                        error: $.alerterror
                    });
            }});
    });
});

})(this.jQuery);

// vim: tabstop=4:shiftwidth=4:expandtab
