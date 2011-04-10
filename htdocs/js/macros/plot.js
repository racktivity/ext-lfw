var render = function(options) {
    var TEMPLATE_NAME = 'plugin.jqplot';
    var $this = $(this);
        
    var cb = function(){
	    $.template(TEMPLATE_NAME, '<div><div id="chartdiv" style="height:700px;width:700px; "></div></div>');
	    $.tmpl(TEMPLATE_NAME, {}).appendTo($this);
	            
        $.jqplot.config.enablePlugins = true;
        $.jqplot('chartdiv',  [[[1, 2],[3,5.12],[5,13.1],[7,33.6],[9,85.9],[11,219.9]]],
                {
                    title:'Exponential Line',
                    axes:{yaxis:{renderer: $.jqplot.LogAxisRenderer, tickDistribution:'power'}},
                    series:[{color:'#d8b83f'}]
                });
            
    };
    options.addDependency(cb, ["/static/lfw/js/libs/jqplot/src/jquery.jqplot.js", "/static/lfw/js/libs/jqplot/src/jqplot.core.js","/static/lfw/js/libs/jqplot/src/jqplot.linearTickGenerator.js",'/static/lfw/js/libs/jqplot/src/jqplot.linearAxisRenderer.js','/static/lfw/js/libs/jqplot/src/jqplot.axisTickRenderer.js','/static/lfw/js/libs/jqplot/src/jqplot.axisLabelRenderer.js','/static/lfw/js/libs/jqplot/src/jqplot.tableLegendRenderer.js','/static/lfw/js/libs/jqplot/src/jqplot.lineRenderer.js','/static/lfw/js/libs/jqplot/src/jqplot.markerRenderer.js','/static/lfw/js/libs/jqplot/src/jqplot.divTitleRenderer.js','/static/lfw/js/libs/jqplot/src/jqplot.canvasGridRenderer.js','js/libs/jqplot/src/jqplot.shadowRenderer.js','/static/lfw/js/libs/jqplot/src/jqplot.shapeRenderer.js','/static/lfw/js/libs/jqplot/src/jqplot.sprintf.js','/static/lfw/js/libs/jqplot/src/jsdate.js',"/static/lfw/js/libs/jqplot/src/jqplot.themeEngine.js", ]);
    options.addCss({'id': 'jqplot', 'tag': 'link', 'params': {'rel': 'stylesheet', 'href': '/static/lfw/js/libs/jqplot/src/jquery.jqplot.css'}});
}
register(render);