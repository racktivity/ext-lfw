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
    var renderer = data_dict.renderer;
    var showTicks = data_dict.showTicks;
    var lineWidth = data_dict.lineWidth;
    var axesMin = data_dict.axesMin;
    var rendererOptions = $.extend({}, data_dict.rendererOptions);
    var xticks = data_dict.xticks || [];
    var yticks = data_dict.yticks || [];
    var xtickformat = data_dict.xtickformat || '';
    var ytickformat = data_dict.ytickformat || '';
    var shadow = data_dict.shadow;
    var renderer_dependency;

    if (renderer) {
        var renderer_name = renderer.replace("$.jqplot.", "");
        renderer_name = renderer_name.charAt(0).toLowerCase().concat(renderer_name.slice(1));
        renderer_dependency = "js/libs/jqplot/src/plugins/jqplot." + renderer_name + ".js";
    }

    console.log("redered_path : " + renderer_dependency);

    var getID = function(){
        return Math.round(Math.random() * 1000000000).toString();
    };

    var chart_div = getID();

    var cb = function(){
        var opts = {
            axesDefaults: { min: axesMin },
            axes: {
                xaxis: {
                    ticks: xticks,
                    tickOptions: { formatString: xtickformat }
                },
                yaxis: {
                    ticks: yticks,
                    tickOptions: { formatString: ytickformat }
                }
            },
            seriesDefaults: {
                lineWidth: lineWidth,
                markerOptions: { show: showTicks }
            },
            grid: {
                shadow: shadow
            }
        };
        if (renderer){
             $.extend(opts, { series: [ { renderer: eval(renderer), rendererOptions: rendererOptions } ] });
        }
        $.jqplot.config.enablePlugins = true;
        $.jqplot(chart_div, chart_data, opts);
    };

    var dependencies = ["js/libs/jqplot/src/jquery.jqplot.js",
     "js/libs/jqplot/src/jqplot.core.js",
     "js/libs/jqplot/src/jqplot.linearTickGenerator.js",
     'js/libs/jqplot/src/jqplot.linearAxisRenderer.js',
     'js/libs/jqplot/src/jqplot.axisTickRenderer.js',
     'js/libs/jqplot/src/jqplot.axisLabelRenderer.js',
     'js/libs/jqplot/src/jqplot.tableLegendRenderer.js',
     'js/libs/jqplot/src/jqplot.lineRenderer.js',
     'js/libs/jqplot/src/jqplot.markerRenderer.js',
     'js/libs/jqplot/src/jqplot.divTitleRenderer.js',
     'js/libs/jqplot/src/jqplot.canvasGridRenderer.js',
     'js/libs/jqplot/src/jqplot.shadowRenderer.js',
     'js/libs/jqplot/src/jqplot.shapeRenderer.js',
     'js/libs/jqplot/src/jqplot.sprintf.js',
     'js/libs/jqplot/src/jsdate.js',
     "js/libs/jqplot/src/jqplot.themeEngine.js"];

    if (renderer_dependency){
        dependencies.push(renderer_dependency);
    }

    width =  isNaN(Number(width)) ? width: width + "px";
    height = isNaN(Number(height)) ? height: height + "px";

    $.template(TEMPLATE_NAME, '<div><div id="${chart_div}" style="height:${height};width:${width}; "></div></div>');
    $.tmpl(TEMPLATE_NAME, { chart_div: chart_div, height: height, width: width }).appendTo($this);

    options.addCss({ 'id': 'jqplot', 'tag': 'link',
        'params': { 'rel': 'stylesheet', 'href': 'js/libs/jqplot/src/jquery.jqplot.css' } });

    options.addDependency(cb, dependencies, true);
};

register(render);

