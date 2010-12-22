var app = $.sammy(function() {
    var _space = null;

    var setSpace = function(space) {
        _space = space;

        var spaces = $('#space option');
        for(var i = 0; i < spaces.length; i++) {
            if(spaces[i].value == space) {
                $(spaces[i]).attr('selected', '1');
            }
        }

        $('form#title-search').attr('action', '#/' + space);
        $('form#label-search').attr('action', '#/' + space);
        $('form#fulltext-search').attr('action', '#/' + space);

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
                var term = request.term.split(/,\s*/).pop();

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

    this.get('#/:space', function() {
        setSpace(this.params['space']);

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
               //TODO Template-based

               var canvas = $('#main'),
                   list = $('<ul>');

               for(var i = 0; i < data.length; i++) {
                   var item = data[i],
                       space = item[0],
                       page = item[1],

                       itemHref = '#/' + space + '/' + page,

                       link = $('<a>').attr('href', itemHref)
                                     .text(page);

                   $('<li>').append(link).appendTo(list);
               }

               canvas.empty().append(list);
           });

        }
        else if(this.params['q']) {
            var page = this.params['q'];

            this.redirect('#/' + getSpace() + '/' + page);
        }
        else {
            this.redirect('#/' + getSpace() + '/Home');
        }
    });

    this.get('#/:space/:page', function() {
        setSpace(this.params['space']);

        var space = this.params['space'],
            page = this.params['page'],
            pageUri = LFW_CONFIG['uris']['pages'] + '/' + space + '/' + page;

        var context = this;

        $.ajax({
            url: pageUri,
            success: function(data) {
                $('#main').html(data['content']);
            },
            cache: false,
            dataType: 'json',
            error: function(xhr, text) {
                if(xhr.status == 404) {
                    context.notFound();
                }
                else {
                    alert('Unknown error: ' + text);
                }
            }
        });
    });

    this.bind('change-space', function(e, data) {
        this.log('change-space');
        this.redirect('#/' + data['space']);
    });

    this.bind('error', function(e, data) {
        $('#main').empty()
                  .html(data.message);
    });
});

$(function() {
    // Set up spaces dropdown
    if(typeof(LFW_CONFIG) === 'undefined' || !LFW_CONFIG) {
        throw new Error('No LFW_CONFIG defined');
    }

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

            app.run('#/' + $('#space').val());
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
                $('form#label-search').submit();

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
                var terms = this.value.split(/,\s*/);
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

            if(!title || title == '') {
                alert('No text');
            }
            else {
                $('form#title-search').submit();
            }

            return false;
        })
        .autocomplete({
            source: []
        });
});
