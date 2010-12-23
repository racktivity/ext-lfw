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

var DEFAULT_PAGE_NAME = 'Home',
    LABELS_RE = /,\s*/,
    LOCATION_PREFIX = '#/';

var app = $.sammy(function(app) {
    this.use('Title');
    this.use('Mustache');

    var _space = null;

    var swap = function(html) {
        $('#main')
            .empty()
            .html(html);
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
                var term = request.term;

                $.getJSON(completionUri, {
                    'space': space,
                    'type': 'title',
                    'term': term
                }, response);
            }
        );

        $('#labels').autocomplete('option', 'source',
            function(request, response) {
                var term = request.term.split(LABELS_RE).pop();

                $.getJSON(completionUri, {
                    'space': space,
                    'type': 'labels',
                    'term': term
                }, response);
            }
        );
    };
    var getSpace = function() {
        if(!_space) {
            throw new Error('Space requested whilst it\'s not set');
        }

        return _space;
    };

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
        clearFields();

        var context = this;

        if(this.params['q'] && this.params['type']) {
            // This is a search request
            var type = this.params['type'],
                query = this.params['q'],

                searchUri = LFW_CONFIG['uris']['search'];

           $.getJSON(searchUri, {
               'type': type,
               'space': getSpace(),
               'q': query
           }, function(data) {
               context.title('Search Results');

               swap(
                   context.mustache(
                       $('#search-result-template').html(),
                       {'results': data}
                   )
               );
           });

        }
        else {
            this.trigger('change-page', {'title': DEFAULT_PAGE_NAME});
        }
    });

    this.get('#/:space/:page', function() {
        setSpace(this.params['space']);
        clearFields();

        var space = this.params['space'],
            page = this.params['page'],
            pageUri = LFW_CONFIG['uris']['pages'] + '/' + space + '/' + page;

        var context = this;

        $.ajax({
            url: pageUri,
            success: function(data) {
                context.title(page);

                swap(data['content']);
            },
            cache: false,
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

    this.bind('change-space', function(e, data) {
        this.log('change-space');
        setSpace(data['space']);
        this.trigger('change-page', {'title': DEFAULT_PAGE_NAME});
    });

    this.bind('error', function(e, data) {
        var error_template = $('#error-template').html();

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
