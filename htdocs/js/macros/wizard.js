var render = function(options) {
	var $this = $(this);    

	var cb = function() {
        var appserver = options.params.appserver || document.domain;
        var title = options.params.title;
        var name = options.params.name;
        var type = options.params.type || "button";
        var element = null;
        var urlitems = document.URL.split("/")
        var idx = urlitems.indexOf(document.domain)
        var appname = options.params.appname || urlitems[idx+1];
        var domain = options.params.domain || urlitems[idx+3];
        var extra = options.params.extra || '';
        //appname, domainName, wizardName, applicationserverIp, extra
        var action = "jswizards.start('" + appname + "', '" + domain + "', '"+name+"', '"+appserver+"', '"+extra+"')";
        if (type == "button"){
            element = $("<button>").attr("onClick", action).text(title);
        }
        else{
            element = $("<a>").attr("href", "javascript:"+action).text(title);
        }
        $this.empty();
        $this.append(element);
        console.log('Being called by someone');
	};
	
    options.addDependency(cb, 
            ['/static/jswizards/js/jswizards_client.js', 
             '/static/jswizards/js/jswizards.js', 
             '/static/jswizards/js/jswizards_oldstyle.js',
             '/static/jswizards/libs/jquery.form.js', 
             '/static/jswizards/libs/jquery.floatbox.1.0.8.js', 
             '/static/jswizards/libs/jquery-datepicker/demo/scripts/jquery.datePicker.js',
             '/static/jswizards/libs/jquery-datepicker/demo/scripts/date.js', 
             '/static/jswizards/libs/jquery.ui.datetimepicker.js',
             '/static/jswizards/libs/jQueryBubblePopup.v2.3.1_2/jquery.bubblepopup.v2.3.1.min.js',
             '/static/jswizards/libs/jquery-tooltip/js/jtip.js']);
	options.addCss({'id': 'jquery-ui', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': '/static/jswizards/style/jquery-ui.css'}});
	options.addCss({'id': 'wizardaction', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': '/static/jswizards/libs/jQueryBubblePopup.v2.3.1_2/jquery.bubblepopup.v2.3.1.css'}});
};
register(render);
