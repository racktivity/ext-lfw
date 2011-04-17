var render = function(options) {
    var TEMPLATE_NAME = 'plugin.jqplot';
    var $this = $(this);
    var data_dict = $.parseJSON(options.body);
    var height = data_dict.height || 700;
    var width = data_dict.width || 700;
    var chart_data = data_dict.chart_data;
    var renderer = data_dict.renderer;
    var renderer_dependency;

    if (renderer){
        var renderer_name = renderer.replace("$.jqplot.", "");
        renderer_name = renderer_name.charAt(0).toLowerCase().concat(renderer_name.slice(1));
        renderer_dependency = "js/libs/jqplot/plugins/jqplot.renderer_name.js".replace("renderer_name", renderer_name)
    }

    console.log("redered_path : " + renderer_dependency);

    var chart_div = data_dict.chart_div
    
    var cb = function(){
        
        var series;
        if (renderer){
             series = { series:[{renderer:eval(renderer)}]};
        }
        $.jqplot.config.enablePlugins = true;
        plot1 = $.jqplot(chart_div, chart_data, series);
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

    options.addDependency(cb, dependencies); 

    $.template(TEMPLATE_NAME, '<div><div id=${chart_div} style="height:${height}px;width:${width}px; "></div></div>');
    $.tmpl(TEMPLATE_NAME, {chart_div:chart_div, height:height, width:width}).appendTo($this);
    
    options.addCss({'id': 'jqplot', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': 'js/libs/jqplot/src/jquery.jqplot.css'}});
}
register(render);

