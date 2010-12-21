var app = $.sammy(function() {
    var _space = null;

    setSpace = function(space) {
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
    }
    getSpace = function() {
        return _space;
    }

    this.get('#/:space', function() {
        setSpace(this.params['space']);

        if(this.params['search'] && this.params['type']) {
            // This is a search request
            alert('Search request');
        }
        else if(this.params['title']) {
            var page = this.params['title'];

            this.redirect('#/' + getSpace() + '/' + page);
        }
        else {
            this.redirect('#/' + getSpace() + '/Home');
        }
    });

    this.get('#/:space/:page', function() {
        setSpace(this.params['space']);

        $('#main').text('Welcome @ ' + this.params['page']);
    });

    this.bind('change-space', function(e, data) {
        this.log('change-space');
        this.redirect('#/' + data['space']);
    });
});

$(function() {
    // Set up spaces dropdown
    var spaces = $('#space');
    for(var i = 0; i < demodata['spaces'].length; i++) {
        $('<option>')
            .attr('value', demodata['spaces'][i])
            .text(demodata['spaces'][i])
            .appendTo(spaces);
    }

    spaces.change(function() {
        app.trigger('change-space', {space: $(this).val()});
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
            source: function(request, response) {
                response($.ui.autocomplete.filter(
                    demodata['labels'], request.term.split(/,\s*/).pop()));
            },
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
            source: demodata['titles']
        });

    app.run('#/' + $('#space').val());
});
