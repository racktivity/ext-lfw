@metadata title=JqPlot Macro
@metadata tagstring=jqplot chart

[new jqplt chart]:http://www.jqplot.com/docs/files/usage-txt.html
[jqPlot Examples]:http://www.jqplot.com/tests/
[line]: #/alkiradocs/LineChart
[bar]: #/alkiradocs/BarChart
[pie]: #/alkiradocs/PieChart
[block]: #/alkiradocs/BlockChart
[bubble]: #/alkiradocs/BubbleChart


#JqPlot Macro 
The `jqplot` is a jQuery plugin to generate pure client-side JavaScript charts in your web pages.


##Parameters
The `jqplot` macro does not use parameters.
The body contains the data to generate the chart.


##Examples

###[Line Chart][line]

    [[jqplot]]
    {"width" : 400,
     "height" : 400,
     "chart_data" : [[[1, 3], [3, 5], [5, 7], [7, 9], [9, 11], [11, 13]]],
    }
    [[/jqplot]]


[[jqplot]]
{"width" : 400,
 "height" : 400,
 "chart_data" : [[[1, 3], [3, 5], [5, 7], [7, 9], [9, 11], [11, 13]]],
}
[[/jqplot]]

<br />

###[Bar Chart][bar]

    [[jqplot]]
    {"width" : 400,
     "height" : 400,
     "chart_data" : [[[1, 2],[2, 4],[3, 6],[4, 8]]],
     "renderer" :"$.jqplot.BarRenderer"
    }
    [[/jqplot]]
    

[[jqplot]]
{"width" : 400,
 "height" : 400,
 "chart_data" : [[[1, 2],[2, 4],[3, 6],[4, 8]]],
 "renderer" :"$.jqplot.BarRenderer"
}
[[/jqplot]]

<br />

###[Pie Chart][pie]
    [[jqplot]]
    {"width" : 400,
     "height" : 400,
     "chart_data" : [[[1, 2],[2, 4],[3, 6],[4, 8]]],
     "renderer" :"$.jqplot.PieRenderer"
    }
    [[/jqplot]]


[[jqplot]]
{"width" : 400,
 "height" : 400,
 "chart_data" : [[[1, 2],[2, 4],[3, 6],[4, 8]]],
 "renderer" :"$.jqplot.PieRenderer"
}
[[/jqplot]]

<br />

###[Block Chart][block]

    [[jqplot]]
    {"width" : 400,
     "height" : 400,
     "chart_data" : [[[1, 2, "red"],[2, 4, "blue"],[3, 6, "blach"],[4, 8,"green"]]],
     "renderer" :"$.jqplot.BlockRenderer"
    }
    [[/jqplot]]


[[jqplot]]
{"width" : 400,
 "height" : 400,
 "chart_data" : [[[1, 2, "red"],[2, 4, "blue"],[3, 6, "blach"],[4, 8,"green"]]],
 "renderer" :"$.jqplot.BlockRenderer"
}
[[/jqplot]]

<br />

###[Bubble Chart][bubble]

    [[jqplot]]
    {"width" : 400,
     "height" : 400,
     "chart_data" : [[[0.6, 2.6, 12, "Ford"], [0.5, 3, 16, "GM"], [1.3, 2, 17, "VW"], [1.2, 1.2, 13, "Mini"]]],
     "renderer" :"$.jqplot.BubbleRenderer"
    }
    [[/jqplot]]


[[jqplot]]
{"width" : 400,
 "height" : 400,
 "chart_data" : [[[0.6, 2.6, 12, "Ford"], [0.5, 3, 16, "GM"], [1.3, 2, 17, "VW"], [1.2, 1.2, 13, "Mini"]]],
 "renderer" :"$.jqplot.BubbleRenderer"
}
[[/jqplot]]

- - -
For more details and examples see [How to create a jqPlot chart][new jqplt chart] and [jqPlot Examples][jqPlot Examples].
