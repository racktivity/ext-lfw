@metadata title=Protovis Macro
@metadata tagstring=macro alkira protovis

[protovis]: http://mbostock.github.com/protovis/

#Protovis Macro
The `protovis` macro creates a zoomable line-graph.


##Parameters
The macro does not use parameters. The body contains the data to generate the chart.


##Example
    [[protovis]]
        {
         "width": 330,
         "data" : [1, 1.2, 1.7, 1.5, 0.7, 0.5, 0.2, -2, -0.4, 0, 3, 1.47, 2, 0, 6],
         "protovis_id" : "protovis_div"
        }
    [[/protovis]]


###Result

[[protovis]]
{
 "width": 330,
 "data" : [1, 1.2, 1.7, 1.5, 0.7, 0.5, 0.2, -2, -0.4, 0, 3, 1.47, 2, 0, 6],
 "protovis_id" : "protovis_div"
}
[[/protovis]]
