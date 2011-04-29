[new jqplt chart]:http://www.jqplot.com/docs/files/usage-txt.html
[jqPlot Examples]:http://www.jqplot.com/tests/

#JqPlot Macro 
jqPlot is a jQuery plugin to generate pure client-side JavaScript charts in your web pages.


##Parameters
The jqplot macro does not use parameters.
The body contains the data to generate the chart.


##Examples

###[Line Chart](/sampleapp/#/alkiradocs/LineChart)
    [[jqplot]]
    {"width" : 400,
     "height" : 400,
     "chart_data" : [[[1, 3], [3, 5], [5, 7], [7, 9], [9, 11], [11, 13]]],
     "chart_div" : "line_div"
    }
    [[/jqplot]]

<br />

[[jqplot]]
{"width" : 400,
 "height" : 400,
 "chart_data" : [[[1, 3], [3, 5], [5, 7], [7, 9], [9, 11], [11, 13]]],
 "chart_div" : "line_div"
}
[[/jqplot]]

<br />

###[Bar Chart](/sampleapp/#/alkiradocs/BarChart)
    [[jqplot]]
    {"width" : 400,
     "height" : 400,
     "chart_data" : [[[1, 2],[2, 4],[3, 6],[4, 8]]],
     "chart_div" : "bar_div",
     "renderer" :"$.jqplot.BarRenderer"
    }
    [[/jqplot]]
    
<br />

[[jqplot]]
{"width" : 400,
 "height" : 400,
 "chart_data" : [[[1, 2],[2, 4],[3, 6],[4, 8]]],
 "chart_div" : "bar_div",
 "renderer" :"$.jqplot.BarRenderer"
}
[[/jqplot]]

<br />

###[Pie Chart](/sampleapp/#/alkiradocs/PieChart)
    [[jqplot]]
    {"width" : 400,
     "height" : 400,
     "chart_data" : [[[1, 2],[2, 4],[3, 6],[4, 8]]],
     "chart_div" : "pie_div",
     "renderer" :"$.jqplot.PieRenderer"
    }
    [[/jqplot]]

<br />

[[jqplot]]
{"width" : 400,
 "height" : 400,
 "chart_data" : [[[1, 2],[2, 4],[3, 6],[4, 8]]],
 "chart_div" : "pie_div",
 "renderer" :"$.jqplot.PieRenderer"
}
[[/jqplot]]

<br />

###[Block Chart](/sampleapp/#/alkiradocs/BlockChart)
    [[jqplot]]
    {"width" : 400,
     "height" : 400,
     "chart_data" : [[[1, 2, "red"],[2, 4, "blue"],[3, 6, "blach"],[4, 8,"green"]]],
     "chart_div" : "block_div",
     "renderer" :"$.jqplot.BlockRenderer"
    }
    [[/jqplot]]

<br />

[[jqplot]]
{"width" : 400,
 "height" : 400,
 "chart_data" : [[[1, 2, "red"],[2, 4, "blue"],[3, 6, "blach"],[4, 8,"green"]]],
 "chart_div" : "block_div",
 "renderer" :"$.jqplot.BlockRenderer"
}
[[/jqplot]]

<br />

###[Bubble Chart](/sampleapp/#/alkiradocs/BubbleChart)
    [[jqplot]]
    {"width" : 400,
     "height" : 400,
     "chart_data" : [[[0.6, 2.6, 12, "Ford"], [0.5, 3, 16, "GM"], [1.3, 2, 17, "VW"], [1.2, 1.2, 13, "Mini"]]],
     "chart_div" : "bubble_div",
     "renderer" :"$.jqplot.BubbleRenderer"
    }
    [[/jqplot]]

<br />

[[jqplot]]
{"width" : 400,
 "height" : 400,
 "chart_data" : [[[0.6, 2.6, 12, "Ford"], [0.5, 3, 16, "GM"], [1.3, 2, 17, "VW"], [1.2, 1.2, 13, "Mini"]]],
 "chart_div" : "bubble_div",
 "renderer" :"$.jqplot.BubbleRenderer"
}
[[/jqplot]]

- - -
For more details and examples see [How to create a jqPlot chart][new jqplt chart] and [jqPlot Examples][jqPlot Examples].
