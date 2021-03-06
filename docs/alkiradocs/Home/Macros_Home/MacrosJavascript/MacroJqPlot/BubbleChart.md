@metadata title=JqPlot Bubble Chart
@metadata order=3
@metadata tagstring=jqplot chart bubble

[jqplot options]:http://www.jqplot.com/docs/files/jqPlotOptions-txt.html#jqPlot_Options
[createmacro]: #/alkiradocs/Macros_HOWTO


# Bubble Chart

The Bubble chart is an example with explanation of the JqPlot Bubble Chart


##The body of the macro is the parameters that JqPlot uses to initialize the block chart.  

* width:- The width of the canvas where the chart is drawn. An optional parameter.  
* height:- The height of the canvas where the chart is drawn. An optional parameter.  
* chart_data:- A list of the bubble set(s) that will be drawn where each bubble set is a list of points.The points must be a list of [x, y, z, 'value'] as x, y are the axes of the point, z is the diameter of the bubble and 'value' is what is written in the bubble. 
  A mandatory parameter.  
* chart_div:- The HTML div that will contain the chart. A mandatory parameter.  
* renderer:- the shape which jqPlot will draw that is the Bubble in this macro. If this parameter is not provided jqPlot will draw the default shape of the bubble chart.


##Example

    [[jqplot]]
        {"width" : 400,
         "height" : 400,
         "chart_data" : [[[0.6, 2.6, 12, "Ford"], [0.5, 3, 16, "GM"],
          [1.3, 2, 17, "VW"], [1.2, 1.2, 13, "Mini"]]],
         "renderer" :"$.jqplot.BubbleRenderer"
        }
    [[/jqplot]]

If you want to create a macro with a more complicated bubble chart please see [How to Create a Macro][createmacro] and [jqPlot options page][jqplot options].
  
  
## Sample Bubble Chart

[[jqplot]]
{"width" : 400,
 "height" : 400,
 "chart_data" : [[[0.6, 2.6, 12, "Ford"], [0.5, 3, 16, "GM"], [1.3, 2, 17, "VW"], [1.2, 1.2, 13, "Mini"]]],
 "renderer" :"$.jqplot.BubbleRenderer"
}
[[/jqplot]]
