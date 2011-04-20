[line chart]:http://www.jqplot.com/tests/coretests.php
# Line Chart

The Line chart is an example with explanation of the JqPlot Line Chart

##Parameters

######The body of the macro is the parameters that JqPlot uses to initialize the line chart.

    1- width:- The width of the canvas where the chart is drawn. An optional parameter.  
    2- height:- The height of the canvas where the chart is drawn. An optional parameter.  
    3- chart_data:- A list of the line(s) that will be drawn where each line is a list of points.  
       The points can be some numbers which jqPlot will consider as the 'y' axis of the point and set  
       the default 'x' axis to them, OR they can be lists of the [x,y] axes of the point  
       A mandatory parameter.  
    4- chart_div:- The HTML div that will contain the chart. A mandatory parameter.  

##Example

    <div class="macro macro_jqplot">
        {"width" : 400,
         "height" : 400,
         "chart_data" : [[[1, 3], [3, 5], [5, 7], [7, 9], [9, 11], [11, 13]]],
         "chart_div" : "line_div",
        }
    </div>
    
If you want to create a macro with a more complicated line chart please see [How to Create a Macro](/sampleapp/#/alkiradocs/Macros_HOWTO) and [jqPlot line chart page][line chart].

<br />

## Sample Line Chart

<div class="macro macro_jqplot">
{"width" : 400,
 "height" : 400,
 "chart_data" : [[[1, 3], [3, 5], [5, 7], [7, 9], [9, 11], [11, 13]]],
 "chart_div" : "line_div"
}
</div>