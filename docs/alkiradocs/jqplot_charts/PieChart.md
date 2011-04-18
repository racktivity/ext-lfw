[pie chart]:http://www.jqplot.com/tests/pieTests.php
# Pie Chart

The Pie Chart is an example with explanation of the JqPlot Pie Chart.  

##Parameters

######The body of the macro is the parameters that JqPlot uses to initialize the pie chart.  
    1- width:- The width of the canvas where the chart is drawn. An optional parameter.  
    2- height:- The height of the canvas where the chart is drawn. An optional parameter.  
    3- chart_data:- A list that contains the pie that will be drawn where the pie is a list of points.  
       The points can be some numbers which jqPlot will consider as the sizes of the pie slices  
       respectively, OR they can be lists of the [slice_name,slice_size]. A mandatory parameter.  
    4- chart_div:- The HTML div that will contain the chart. A mandatory parameter.  
    5- renderer:- the shape which jqPlot will draw that is the Pie in this macro. If this parameter is  
       not passed jqPlot will draw the default shape the Line chart.


##Example
    <div class="macro macro_jqplot">
        {"width" : 400,
         "height" : 400,
         "chart_data" : [[[1, 2],[2, 4],[3, 6],[4, 8]]],
         "chart_div" : "pie_div",
         "renderer" :"$.jqplot.PieRenderer"
        }
    </div>
######If you want to create a macro with a more complicated bar chart please see [How to Create a Macro](/sampleapp/#/alkiradocs/Macros_HOWTO)  
######and [jqPlot pie chart page][pie chart]
## Sample
### Pie Chart
<div class="macro macro_jqplot">
{"width" : 400,
 "height" : 400,
 "chart_data" : [[[1, 2],[2, 4],[3, 6],[4, 8]]],
 "chart_div" : "pie_div",
 "renderer" :"$.jqplot.PieRenderer"
}
</div>