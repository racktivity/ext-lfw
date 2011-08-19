@metadata title=JqPlot Block Chart
@metadata order=2
@metadata tagstring=jqplot chart block

[jqplot options]:http://www.jqplot.com/docs/files/jqPlotOptions-txt.html#jqPlot_Options
[createmacro]: #/alkiradocs/Macros_HOWTO


# Block Chart

The Block chart is an example with explanation of the JqPlot Block Chart


##The body of the macro is the parameters that JqPlot uses to initialize the block chart.

* width:- The width of the canvas where the chart is drawn. An optional parameter.  
* height:- The height of the canvas where the chart is drawn. An optional parameter.  
* chart_data:- A list of the block set(s) that will be drawn where each block set is a list of points. The points must be a list of [x, y, 'value'] as x, y are the axes of the point and 'value' is what is written in the block. 
  A mandatory parameter.  
* chart_div:- The HTML div that will contain the chart. A mandatory parameter.  
* renderer:- the shape which jqPlot will draw that is the Block in this macro. If this parameter is not provided jqPlot will draw the default shape of the block chart.


##Example

    [[jqplot]]
        {"width" : 400,
         "height" : 400,
         "chart_data" : [[[1, 2, "red"],[2, 4, "blue"],[3, 6, "blach"],[4, 8,"green"]]],
         "renderer" :"$.jqplot.BlockRenderer"
        }
    [[/jqplot]]

If you want to create a macro with a more complicated block chart please see [How to Create a Macro][createmacro] and [jqPlot options page][jqplot options].

  
## Sample Block Chart

[[jqplot]]
{"width" : 400,
 "height" : 400,
 "chart_data" : [[[1, 2, "red"],[2, 4, "blue"],[3, 6, "blach"],[4, 8,"green"]]],
 "renderer" :"$.jqplot.BlockRenderer"
}
[[/jqplot]]
