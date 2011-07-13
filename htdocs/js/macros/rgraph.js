//@metadata wizard=rgraph

var render = function(options) {
    var TEMPLATE_NAME = 'plugin.rgraph';
    var $this = $(this);
    var data_dict = options.body ? $.parseJSON(options.body) : options.params;
    var chart_div = data_dict.chart_div;
    var height = data_dict.height || 300;
    var width = data_dict.width || 280;
    var values = data_dict.values;
    var time = new Date().getTime();
    var computed = false;

    var _findParent = function (data, parent, depth) {
        var d = data.depth;
        var nodes = (function getChildren(data, d) {
            var children = data.children,
                i = 0, nodes = [];
            if (children) {
                for (i = 0; i < children.length; i++) {
                    var child = children[i];
                    d = child.depth;
                    if (d < depth) {
                        $.merge(nodes, getChildren(child, d));
                    } else {
                        nodes.push(child);
                    }
                }
            }
            return nodes;
        })(data, d);
        var i;
        for (i = 0; i < nodes.length; ++i) {
            var node = nodes[i];
            if (node.id === parent.id) {
                return node;
            }
        }
        return undefined;
    };

    var _convertData = function _convertData(data, parent, depth) {
        depth = depth ? depth : 0;
        var new_id = "";
        if (typeof(parent) === 'undefined') {
            new_id = time + "_0";
            data.id = new_id;
            parent = {
                "id": new_id,
                "name": data.name,
                "data": {
                    "$type": "star",
                    "$dim": 8,
                    "depth": data.depth,
                    "has_children": $.isArray(data.children)
                }
            };
        }
        // Find parent in data
        if (depth > 0) {
            data = _findParent(data, parent, depth);
        }
        parent.children = [];
        var children = data.children;
        if (children) {
            var i = 0;
            for (i = 0; i < children.length; i++) {
                var child = children[i];
                new_id =  parent.id + "_" + i;
                child.id = new_id;
                var new_child = {
                    "id": new_id,
                    "name": child.name,
                    data: { "depth": child.depth, "has_children": ( $.isArray(child.children) &&
                            child.children.length > 0 ) }
                };
                parent.children.push(new_child);
            }
        }
        return parent;
    };

    var json = _convertData(values.root);

    var _getColor = function(node) {
        var colors = {};
        colors.company = "#FF0000";
        colors.campus = "darkgreen";
        colors.building = "gold";
        colors.floor = "purple";
        colors.room = "blue";
        colors.pod = "orange";
        colors.rack = "black";
        colors.pdu = "#FF0000";
        switch (node.data.depth) {
            case 0:
                return colors.company;
            case 1:
                return colors.campus;
            case 2:
                return colors.building;
            case 3:
                return colors.floor;
            case 4:
                return colors.room;
            case 5:
                return colors.pod;
            case 6:
                return colors.rack;
            case 7:
                return colors.pdu;
            default:
                return colors.company;
        }
    };

    var _getTextColor = function(node, rgb) {
        var total = rgb.r + rgb.g + rgb.b;
        if (total > (3 * 256 / 2)) {
            return "#000000";
        } else {
            return "#FFFFFF";
        }
    };

    var _collapseSubNodes = function _collapseSubNodes(rgraph, node, useAnimation) {
        var subs, sub;
        //check if we have subnodes
        subs = node.getSubnodes([1, 1]);
        //collapse subnodes that are open
        var i;
        for (i = 0; i < subs.length; ++i) {
            sub = subs[i];
            if (sub.data.depth > node.data.depth && !sub.collapsed) {
                if (sub.getSubnodes([1, 1]).length > 1) { //if we have subnodes then collapse
                    rgraph.op.contract(sub, {type: useAnimation ? "animate" : "replot"});
                    //sub.collapsed = true;
                }
            }
        }
    };

    var callBack = function callBack() {
        var rgraph = new $jit.RGraph({
            injectInto: chart_div,
            width: width,
            height: height,
            duration: 300,
            levelDistance: 70,
            interpolation: "linear",
            Navigation: {
                enable: true,
                zooming: 100
            },
            Node: {
                overridable: true,
                color: "#FF0000"
            },
            Edge: {
                lineWidth: 1.5,
                color: "#0071B5"
            },
            onCreateLabel: function(domElement, node) {
                domElement.innerHTML = node.name;
                domElement.onclick = function() {
                    computed = false;
                    rgraph.onClick(node.id);
                };

                this.onPlaceLabel(domElement, node);
            },
            onAfterCompute: function() {
                if (!computed) {
                    computed = true;
                    var node = rgraph.graph.getClosestNodeToOrigin("current"),
                        subs, sub;

                    if (node.collapsed === true) { //expand node first if we are collapsed
                        //manually fix the subnodes as expand isn't working fully
                        subs = node.getSubnodes(2);
                        var j;
                        for (j=0;j<subs.length;j++) {
                            sub = subs[j];
                            delete sub.ignore;
                            sub.setData("alpha", 1, "end");
                        }
                        rgraph.op.expand(node, { type: "animate" });
                    } else {
                        //check if we have subnodes
                        subs = node.getSubnodes([1, 1]);
                        if (subs.length === 1) { //we only have 1 "subnode" which is our parent (strangely enough)
                            var json = _convertData(values.root, node, node.data.depth);
                            if (json !== undefined) { //append our now data to the current graph
                                rgraph.op.sum(json, { type: "fade" });
                            }
                        } else {
                            _collapseSubNodes(rgraph, node, true);
                        }

                    }
                }
            },
            onPlaceLabel: function(domElement, node) {
                var style = domElement.style;
                var depth = node.data.has_children ? 1 : 2;
                if (node._depth <= depth) { //set the right color for the labels
                    style.backgroundColor = _getColor(node);
                    style.color = _getTextColor(node, style.backgroundColor);
                    style.display = "";
                } else { //hide the labels
                    style.display = "none";
                }
                var left = parseInt(style.left, 10);
                var top = parseInt(style.top, 10);
                var w = domElement.offsetWidth;
                var h = domElement.height;
                style.left = (left - w / 2) + 'px';
                style.top = (top - h / 2) + 'px';
            },
            onBeforePlotNode: function(node) {
                node.setData("color", _getColor(node));
            }
        });

        rgraph.canvas.scale(1 / rgraph.canvas.scaleOffsetX, 1 / rgraph.canvas.scaleOffsetY);

        rgraph.loadJSON(json);
        rgraph.compute();
        _collapseSubNodes(rgraph, rgraph.graph.getNode(rgraph.root), false);
        rgraph.refresh();
    };

    $.template(TEMPLATE_NAME, '<div><div id=${chart_div} style="height:${height}px;width:${width}px; "></div></div>');
    $.tmpl(TEMPLATE_NAME, {chart_div:chart_div, height:height, width:width}).appendTo($this);

    options.addCss({'id': 'rgraphmacro', 'tag': 'style', 'params': '.node { cursor: pointer; padding: 0em 0.3em }'});

    options.addDependency(callBack, ["/static/lfw/js/libs/Jit-2.0.0b/jit.js"]);
};
register(render);
