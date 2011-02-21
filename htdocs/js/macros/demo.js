var render = function(options) {
    var text = (options.options['text'] || 'Demo') + '!',
        $this = $(this);

    if(options.space)
        text += ' Welcome in space ' + options.space + '.';

    if(options.page)
        text += ' You\'re on page <strong>' + options.page + '</strong>!';

    $this.append(
        $('<h1>').html(text)
    );

    setTimeout(function() {
        $this.fadeOut(3000);
    }, 2000);
}

register(render);
