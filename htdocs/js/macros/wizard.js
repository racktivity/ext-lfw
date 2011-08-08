//@metadata wizard=wizard
//@metadata description=Shows a button for wizard start-up
//@metadata image=img/macros/wizard.png
//@metadata documentationUrl=http://www.pylabs.org/#/alkiradocs/MacroWizard

var render = function(options) {
    var $this = $(this);

    var cb = function() {
        var appserver = options.params.appserver || document.domain;
        var title = options.params.title;
        var name = options.params.name;
        var type = options.params.type || "button";
        var element = null;
        var urlitems = document.location.href.split("/")
        var idx = urlitems.indexOf(document.domain)
        var appname = options.params.appname || urlitems[idx+1];
        var domain = options.params.domain || options.space;
        var extra = options.params.extra || '';
        var service = options.params.service || null;
        if (!service){
            var service = "http://" + appserver + "/" + appname + "/appserver/rest/ui/wizard";
        }

        var action = "JSWizards.launch('" + service + "', '" + domain + "', '" + name + "', '" + extra +"')";
        if (type == "button"){
            element = $("<button>");
        }
        else{
            element = $("<a>").attr("href", "javascript:void(0)");
        }
        element.attr("onClick", action).text(title);
        $this.attr('style', 'float: left; width: auto');
        $this.append(element);
    };

    options.addDependency(cb,
            ['/static/jswizards/ext/jquery-ui.min.js',
             '/static/jswizards/js/jswizards.js',
             '/static/jswizards/ext/jquery.floatbox.1.0.8.js',
             '/static/jswizards/ext/jquery.ui.datetimepicker.js']);
    options.addCss({'id': 'jquery-ui', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': '/static/jswizards/ext/jquery-ui.css'}});
    options.addCss({'id': 'floatbox-wizard', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': '/static/jswizards/ext/joshuaclayton-blueprint-css-c20e981/blueprint/screen.css'}});
        options.addCss({'id': 'floatbox-wizard-btn', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': '/static/jswizards/ext/joshuaclayton-blueprint-css-c20e981/blueprint/plugins/buttons/screen.css'}});
    options.addCss({'id': 'wizardaction', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': '/static/jswizards/style/screen.css'}});
};
register(render);
