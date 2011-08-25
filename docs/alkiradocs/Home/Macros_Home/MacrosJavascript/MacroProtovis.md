@metadata title=Protovis Macro
@metadata tagstring=macro alkira protovis

[protovis]: http://mbostock.github.com/protovis/

#Protovis Macro
The `protovis` macro creates a zoomable line-graph where you provide the Y-values. These are automatically linked to default X-values.
The values of your graphic are stored in a list. If you provide a list of lists, then you have a graphic for each list, but now displayed in one graph. This allows you to easily compare two sets of data.


##Parameters
The macro does not use parameters. The body contains the data to generate the chart.
The data provided in the body of the macro are the values of the Y-axis. Each provided Y-values corresponds with a complete unit of the X-axis, starting with 0 on the X-axis.
In the example below, Y-value 1.7 corresponds with an X-value of 2.

Below the graphic, you can scroll through your graphic and gives you an overview of the complete graph.


##Example

Example for a graphic with one data stream:

    [[protovis]]
        {
         "width": 330,
         "data" : [1, 1.2, 1.7, 1.5, 0.7, 0.5, 0.2, -2, -0.4, 0, 3, 1.47, 2, 0, 6, 4.5],
         "protovis_id" : "protovis_div"
        }
    [[/protovis]]
    
    
Example for a graphic with two data streams:

    [[protovis]]
    {
     "width": 330,
     "data" : [[1, 1.2, 1.7, 1.5, 0.7, 0.5, 0.2, -2], [-0.4, 0, 3, 1.47, 2, 0, 6, 4.5]],
     "protovis_id" : "protovis_div"
    }
    [[/protovis]]


##Sample

Sample for a graphic with one data stream:
[[protovis]]
{
 "width": 330,
 "data" : [1, 1.2, 1.7, 1.5, 0.7, 0.5, 0.2, -2, -0.4, 0, 3, 1.47, 2, 0, 6],
 "protovis_id" : "protovis_div"
}
[[/protovis]]


Sample for a graphic with two data streams:
[[protovis]]
{
 "width": 330,
 "data" : [[1, 1.2, 1.7, 1.5, 0.7, 0.5, 0.2, -2], [-0.4, 0, 3, 1.47, 2, 0, 6, 4.5]],
 "protovis_id" : "protovis_div"
}
[[/protovis]]
