[new jqplt chart]:http://www.jqplot.com/docs/files/usage-txt.html
[jqPlot Examples]:http://www.jqplot.com/tests/

# JqPlot Macro 

jqPlot is a jQuery plugin to generate pure client-side javascript charts in your web pages

##Examples

### [Line Chart](/#/alkiradocs/LineChart)
<div class="macro macro_jqplot">
{"width" : 400,
 "height" : 400,
 "chart_data" : [[[1, 3], [3, 5], [5, 7], [7, 9], [9, 11], [11, 13]]],
 "chart_div" : "line_div"
}
</div>

<br />

### [Bar Chart](/#/alkiradocs/BarChart)
<div class="macro macro_jqplot">
{"width" : 400,
 "height" : 400,
 "chart_data" : [[[1, 2],[2, 4],[3, 6],[4, 8]]],
 "chart_div" : "bar_div",
 "renderer" :"$.jqplot.BarRenderer"
}
</div>
<br />

### [Pie Chart](/#/alkiradocs/PieChart)
<div class="macro macro_jqplot">
{"width" : 400,
 "height" : 400,
 "chart_data" : [[[1, 2],[2, 4],[3, 6],[4, 8]]],
 "chart_div" : "pie_div",
 "renderer" :"$.jqplot.PieRenderer"
}
</div>


### [Block Chart](/#/alkiradocs/BlockChart)
<div class="macro macro_jqplot">
{"width" : 400,
 "height" : 400,
 "chart_data" : [[[1, 2, "red"],[2, 4, "blue"],[3, 6, "blach"],[4, 8,"green"]]],
 "chart_div" : "block_div",
 "renderer" :"$.jqplot.BlockRenderer"
}
</div>
<br />

### [Bubble Chart](/#/alkiradocs/BubbleChart)
<div class="macro macro_jqplot">
{"width" : 400,
 "height" : 400,
 "chart_data" : [[[0.6, 2.6, 12, "Ford"], [0.5, 3, 16, "GM"], [1.3, 2, 17, "VW"], [1.2, 1.2, 13, "Mini"]]],
 "chart_div" : "bubble_div",
 "renderer" :"$.jqplot.BubbleRenderer"
}
</div>

<br />
####For more details and examples see
[How to create a jqPlot chart][new jqplt chart] and [jqPlot Examples][jqPlot Examples]
