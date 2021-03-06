//@metadata wizard=wizard
//@metadata description=Shows a button for wizard start-up
//@metadata image=img/macros/wizard.png
//@metadata documentationUrl=http://www.pylabs.org/#/alkiradocs/MacroWizard

var render = function(options) {
    var $this = $(this);

    var cb = function() {
        var name = options.params.name;
        if (!name){
            //when we are calling macro just to load the dependencies dont render a button
            return;
        }
        var appserver = options.params.appserver || document.domain;
        var title = options.params.title;
        var type = options.params.type || "button";
        var element = null;
        var urlitems = document.location.href.split("/")
        var idx = urlitems.indexOf(document.domain)
        var appname = options.params.appname || urlitems[idx+1];
        var domain = options.params.domain || options.space;
        var extra = options.params.extra || '';
        var service = options.params.service || null;
        var refresh = options.params.refresh === "true" ? true : false; //default false
        
        if (!service){
            var service = "http://" + appserver + "/" + appname + "/appserver/rest/ui/wizard";
        }

        var action = "JSWizards.launch('" + service + "', '" + domain + "', '" + name + "', '" + extra +"', undefined, undefined, " + refresh + ")";
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
            ['jswizards/ext/jquery-ui.min.js',
             'jswizards/js/jswizards.js',
             'jswizards/ext/jquery.floatbox.1.0.8.js',
             'jswizards/ext/jquery.ui.datetimepicker.js']);
    options.addCss({'id': 'jquery-ui', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': 'jswizards/ext/jquery-ui.css'}});
    options.addCss({'id': 'floatbox-wizard', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': 'jswizards/ext/joshuaclayton-blueprint-css-c20e981/blueprint/screen.css'}});
        options.addCss({'id': 'floatbox-wizard-btn', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': 'jswizards/ext/joshuaclayton-blueprint-css-c20e981/blueprint/plugins/buttons/screen.css'}});
    options.addCss({'id': 'wizardaction', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': 'jswizards/style/screen.css'}});
};
register(render);
