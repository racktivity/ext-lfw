(function($) {
    var cache = {};
    var keyre = /^\s*(?:(\w+):)?\s*(\w+(?:\.\w+)*)$/;
    var guessLocale = function(){
        var locale = $.cookie("jquery.language");
        if (locale)
            return locale;
        
        //guess via browser
        locale = navigator.language;
        if (locale) {
            locale = locale.split("-")[0];
            return locale;
        }
        
        return "en";
    };
    
    var query = function (key, package) {
        var kparts = key.split(".");
        var domain = package.sub;
        if (domain == undefined){
            return key;
        };
        while(kparts.length) {
            var part = kparts.shift();
            if (!(part in domain)){
                break;
            }
            domain = domain[part];
            if (kparts.length == 0){
                //no more key parts this should be the value we are searching for.
                if (domain.value != undefined) {
                    return domain.value;
                }
            } else {
                domain = domain.sub
                if (domain == undefined){
                    break;
                }
            }
        }
        //if the key was not found, return the key itself.
        return key;
    };
    
    var download = function(packagekey){
        var url = "js/lang/" + packagekey + ".json";
        var package = {};
        $.ajax(url, {async: false,
                     dataType: 'json'})
            .success(function(_package){
                console.log("package downloaded");
                package = _package;
            })
            .error(function(req, status, msg){
                console.log("Error while downloading '" + url + "': " + msg);
            });
        
        return package;
    };
    
    $.language = function(key, settings){
        var m = keyre.exec(key)
        if (!m) {
            return key;
        }
        
        package = m[1];
        key = m[2];
        
        if (package === undefined){
            package = 'default';
        }
        
        var options = {package: package,
                       forceload: false,
                      locale: guessLocale()};
        
        if (typeof settings === "string"){
            options = $.extend(options, {package: settings});
        } else if ($.isPlainObject(settings)) {
            options = $.extend(options, settings);
        }
        
        var packagekey = options.package + "-" + options.locale;
        
        if (packagekey in cache && !options.forceload) {
            return query(key, cache[packagekey]);
        } else {
            //download the package into the cache
            package = download(packagekey);
            cache[packagekey] = package;
            return query(key, package);
        }
    };
    
})(jQuery);
