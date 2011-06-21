var render = function(options) {
    var $this = $(this);
    var params = $.extend({click: '',
                           href: '',
                           name: '',
                           title: '',
                           target: '',
                           icon: ''}, options.params);
                           
    var btn = $("<a>", {href: params.href,
                        title: params.title,
                        target: params.target,
                        'class': "ui-button ui-widget ui-state-default ui-corner-all ui-button-text-icon-primary",
                        role: 'button',
                        'aria-disabled': 'false'})
                .append($("<span>", {'class': "ui-button-icon-primary ui-icon " + params.icon}))
                .append($("<span>", {'class': "ui-button-text"}).text(params.name))
                .click(function(){
                    eval(params.click);
                });
                
    $this.empty();
    $this.append(btn);
};

register(render);
