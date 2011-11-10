//@metadata wizard=jqplot
//@metadata description=Plots charts (bars, pie, etc.)
//@metadata image=img/macros/jqplot.png
//@metadata documentationUrl=http://www.pylabs.org/#/alkiradocs/MacroJqPlot

var render = function(options) {
    var TEMPLATE_NAME = 'plugin.jqplot';
    var $this = $(this);
    var data_dict = $.parseJSON(options.body);
    var height = data_dict.height || 700;
    var width = data_dict.width || 700;
    var chart_data = data_dict.chart_data;
    var seriesDefaults = data_dict.seriesDefaults;
    var axesDefaults = data_dict.axesDefaults;
    var axes = data_dict.axes;
    var renderer = data_dict.renderer;
	var rendererOptions = $.extend({}, data_dict.rendererOptions);
    var renderer_dependency = [];
    
    if (renderer){
        var renderer_name = renderer.replace("$.jqplot.", "");
        renderer_name = renderer_name.charAt(0).toLowerCase().concat(renderer_name.slice(1));
        renderer_dependency.push("/static/lfw/js/libs/jqplot/src/plugins/jqplot.renderer_name.js".replace("renderer_name", renderer_name));
    }

    console.log("redered_path : " + renderer_dependency);

    var getID = function(){
        return Math.round(Math.random() * 1000000000).toString();
    };

    var chart_div = getID();

    var cb = function(){
        
        var opt = {seriesDefaults: seriesDefaults,
                   axesDefaults: axesDefaults,
                   axes: axes};
        if (renderer){
             $.extend(opt,{ series:[{renderer:eval(renderer),
                                    rendererOptions: rendererOptions}],
                            });
        }
        $.jqplot.config.enablePlugins = true;
        plot1 = $.jqplot(chart_div, chart_data, opt);
    };

    var dependencies = ["/static/lfw/js/libs/jqplot/src/jquery.jqplot.js",
     "/static/lfw/js/libs/jqplot/src/jqplot.core.js",
     "/static/lfw/js/libs/jqplot/src/jqplot.linearTickGenerator.js",
     '/static/lfw/js/libs/jqplot/src/jqplot.linearAxisRenderer.js',
     '/static/lfw/js/libs/jqplot/src/jqplot.axisTickRenderer.js',
     '/static/lfw/js/libs/jqplot/src/jqplot.axisLabelRenderer.js',
     '/static/lfw/js/libs/jqplot/src/jqplot.tableLegendRenderer.js',
     '/static/lfw/js/libs/jqplot/src/jqplot.lineRenderer.js',
     '/static/lfw/js/libs/jqplot/src/jqplot.markerRenderer.js',
     '/static/lfw/js/libs/jqplot/src/jqplot.divTitleRenderer.js',
     '/static/lfw/js/libs/jqplot/src/jqplot.canvasGridRenderer.js',
     '/static/lfw/js/libs/jqplot/src/jqplot.shadowRenderer.js',
     '/static/lfw/js/libs/jqplot/src/jqplot.shapeRenderer.js',
     '/static/lfw/js/libs/jqplot/src/jqplot.sprintf.js',
     //'/static/lfw/js/libs/jqplot/src/plugins/jqplot.pointLabels.js',
     '/static/lfw/js/libs/jqplot/src/jsdate.js',
     "/static/lfw/js/libs/jqplot/src/jqplot.themeEngine.js"];

    if (renderer_dependency){
        dependencies.concat(renderer_dependency);
    }


    $.template(TEMPLATE_NAME, '<div><div id="${chart_div}" style="height:${height}px;width:${width}px; "></div></div>');
    $.tmpl(TEMPLATE_NAME, {chart_div:chart_div, height:height, width:width}).appendTo($this);

    options.addCss({'id': 'jqplot', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': 'js/libs/jqplot/src/jquery.jqplot.css'}});

    options.addDependency(cb, dependencies, true);
}
register(render);

