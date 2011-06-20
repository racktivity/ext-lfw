@metadata title=JqPlot Line Chart
@metadata order=4
@metadata tagstring=jqplot chart line

[line chart]:http://www.jqplot.com/tests/coretests.php
[createmacro]: /#/alkiradocs/Macros_HOWTO

# Line Chart

The Line chart is an example with explanation of the JqPlot Line Chart


##The body of the macro is the parameters that JqPlot uses to initialize the line chart.

* width:- The width of the canvas where the chart is drawn. An optional parameter.  
* height:- The height of the canvas where the chart is drawn. An optional parameter.  
* chart_data:- A list of the line(s) that will be drawn where each line is a list of points. The points can be some numbers which jqPlot will consider as the 'y' axis of the point and set the default 'x' axis to them, OR they can be lists of the [x,y] axes of the point.
  A mandatory parameter.  
* chart_div:- The HTML div that will contain the chart. A mandatory parameter.  


##Example

    [[jqplot]]
        {"width" : 400,
         "height" : 400,
         "chart_data" : [[[1, 3], [3, 5], [5, 7], [7, 9], [9, 11], [11, 13]]],
         "chart_div" : "line_div",
        }
    [[/jqplot]]
    
If you want to create a macro with a more complicated line chart please see [How to Create a Macro][createmacro] and [jqPlot line chart page][line chart].


## Sample Line Chart

[[jqplot]]
{"width" : 400,
 "height" : 400,
 "chart_data" : [[[1, 3], [3, 5], [5, 7], [7, 9], [9, 11], [11, 13]]],
 "chart_div" : "line_div"
}
[[/jqplot]]
