//@metadata wizard=wizard

// Read a page's GET URL variables and return them as an associative array.
function getUrlVars() {
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++) {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}

var render = function(options) {
    var $this = $(this);

    var cb = function() {
        var urlVars = getUrlVars();
        var urlitems = document.URL.split("/")
        var idx = urlitems.indexOf(document.domain)

        var appserver = urlVars.appserver || document.domain;
        var name = urlVars.name;
        var appname = urlVars.appname || urlitems[idx+1];
        var domain = urlVars.domain || urlitems[idx+3];
        var extra = urlVars.extra || '';
        var service = urlVars.service || null;
        if (!service){
            var service = "http://" + appserver + "/" + appname + "/appserver/rest/ui/wizard";
        }

        JSWizards.launch(service, domain, name, extra, function() {
            window.close();
        }, function() {
            window.close();
        });

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
