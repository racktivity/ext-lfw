@metadata title=RGraph Macro
@metadata tagstring=macro alkira rgraph infovis

[Javascript Infovis Toolkit]: http://thejit.org/
[rgraph]: 

#RGraph Macro
The RGraph macro creates an [rgraph][], which is a powerful graphics visualization. The data of the graph is stored in a JSON data structure.


##Parameters
The macro does not use parameters. The body contains the data to generate the rgraph. For advanced examples of RGraphs, see [thejit.org][rgraph].


##Example

    [[rgraph]]
        {"name": "Macros_Home",
         "chart_div": "bar_div",
         "values": {
            "root": {
                "name":"Root Node",
                "depth": 0,
                "children": [
                    {
                        "name": "child 1",
                        "depth": 1,
                        "children": [
                            {
                                "name": "child 1.1",
                                "depth": 2
                            }, {
                                "name": "child 1.2",
                                "depth": 2
                            }
                        ]
                    }, {
                        "name": "child 2",
                        "depth": 1,
                        "children": [
                            {
                                "name": "child 2.1",
                                "depth": 2
                            }, {
                                "name": "child 2.2",
                                "depth": 2
                            }
                        ]
                    }
                ]
            }
         }
        }
    [[/rgraph]]
    

##Sample

[[rgraph]]
{"name": "Macros_Home",
 "chart_div": "bar_div",
 "values": {
    "root": {
        "name":"Root Node",
        "depth": 0,
        "children": [
            {
                "name": "child 1",
                "depth": 1,
                "children": [
                    {
                        "name": "child 1.1",
                        "depth": 2
                    }, {
                        "name": "child 1.2",
                        "depth": 2
                    }
                ]
            }, {
                "name": "child 2",
                "depth": 1,
                "children": [
                    {
                        "name": "child 2.1",
                        "depth": 2
                    }, {
                        "name": "child 2.2",
                        "depth": 2
                    }
                ]
            }
        ]
    }
 }
}
[[/rgraph]]
