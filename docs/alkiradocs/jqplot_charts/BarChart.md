[bar chart]:http://www.jqplot.com/tests/barRendererTests.php
# Bar Chart

The Bar Chart is an example with explanation of the JqPlot Bar Chart.  
Bar charts are rendered with the barRenderer plugin which will be set in the body.

##Parameters

######The body of the macro is the parameters that JqPlot uses to initialize the bar chart.  
    1- width:- The width of the canvas where the chart is drawn. An optional parameter.  
    2- height:- The height of the canvas where the chart is drawn. An optional parameter.  
    3- chart_data:- A list of the bar(s) that will be drawn where each bar is a list of points.  
       The points can be some numbers which jqPlot will consider as the 'y' axis of the point and set  
       the default 'x' axis to them, OR they can be lists of the [x,y] axes of the point  
       A mandatory parameter.  
    4- chart_div:- The HTML div that will contain the chart. A mandatory parameter.  
    5- renderer:- the shape which jqPlot will draw that is the Bar in this macro. If this parameter is  
       not passed jqPlot will draw the default shape the Line chart.


##Example
    <div class="macro macro_jqplot">
        {"width" : 400,
         "height" : 400,
         "chart_data" : [[[1, 2],[2, 4],[3, 6],[4, 8]]],
          "chart_div" : "bar_div",
          "renderer" :"$.jqplot.BarRenderer"
        }
    </div>
    
    
If you want to create a macro with a more complicated bar chart please see [How to Create a Macro](/sampleapp/#/alkiradocs/Macros_HOWTO) and [jqPlot bar chart page][bar chart].

<br />

## Sample Bar Chart

<div class="macro macro_jqplot">
{"width" : 400,
 "height" : 400,
 "chart_data" : [[[1, 2],[2, 4],[3, 6],[4, 8]]],
 "chart_div" : "bar_div",
 "renderer" :"$.jqplot.BarRenderer"
}
</div>