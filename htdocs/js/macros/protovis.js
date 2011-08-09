//@metadata wizard=protovis
//@metadata description=Plots charts
//@metadata image=img/macros/protovis.png
//@metadata documentationUrl=http://www.pylabs.org/#/alkiradocs/MacroProtovis

var render = function(options) {
    var TEMPLATE_NAME = 'plugin.protovis'; // this is only local I think
    var $this = $(this);
    var data_dict = $.parseJSON(options.body);
    var height = data_dict.height || 300;
    var width = data_dict.width || 260;
    
    var data = data_dict.data; // like this: [1, 1.2, 1.7, 1.5, .7, .5, .2]
    var horz_unit = data_dict.horz_unit || 40; // should we name this like this?
    var horz_offset = data_dict.horz_offset || 0;
    var vert_unit = data_dict.vert_unit || 80;
    var label = data_dict.label || "";
    var labelOffset = label ? 20: 0;

    var getID = function(){
        return Math.round(Math.random() * 1000000000).toString();
    };
    
    var protovis_id = getID();
    var roundNumber = function (num) {
        var dec = 1;
        var result = Math.round(num*Math.pow(10,dec))/Math.pow(10,dec);
        return result;
    }

    var getData = function() {
        if (data) {
            var maxData = data,
                minData = data,
                longestData = data,
                _maxY = 0, _minY = 0;

            if ($.isArray(data[0])) {
                maxData = data[0];
                minData = data[0];
                longestData = data[0];
                var i = 0, maxY, minY;
                for (i = 0; i < data.length; i++) {
                    d = data[i];
                    _maxY = Math.max.apply(null, d);
                    _minY = Math.min.apply(null, d);
                    if (_maxY > Math.max.apply(null, maxData)) {
                        maxData = d;
                    }
                    if (_minY < Math.min.apply(null, minData)) {
                        minData = d;
                    }
                    if (d.length > longestData.length) {
                        longestData = d;
                    }
                }
            }
            return {'minData': minData, 'maxData': maxData, 'longestData': longestData};
        }
        return undefined;
    };

    var cb = function() {
        var _data = getData();
        var minY = Math.min.apply(null, _data.minData),
            maxY = Math.max.apply(null, _data.maxData),
            yRange = maxY - minY,
            w = width,
            h1 = height - 45 - 30 - labelOffset,
            h2 = 30,
            x = pv.Scale.linear(0, _data.longestData.length).range(0, w),
            y = pv.Scale.linear(minY - (yRange * 0.1), maxY + (yRange * 0.1)).range(0, h2);

        var focusStartRange = {
            x: w * 0.33,
            dx: w * 0.33
        },
        fx = pv.Scale.linear().range(0, w),
        fy = pv.Scale.linear().range(0, h1);

        var c = pv.Colors.category10();

        $.template(TEMPLATE_NAME, '<div id=${protovis_id} style="height:${height}px;width:${width}px; "></div>');
        $.tmpl(TEMPLATE_NAME, {protovis_id:protovis_id, height:height, width:width}).appendTo($this);

        /* Root Panel */
        var vis = new pv.Panel()
            .canvas(protovis_id)
            .width(width)
            .height(height - 25)
            .left(20)
            .bottom(25);

        vis.anchor("center").add(pv.Label)
            .top(10)
            .textAlign("center")
            .font("20px sans-serif")
            .text(label);

        /* Focus Panel */
        var focus = vis.add(pv.Panel).def("init", function(){
            var d1 = x.invert(focusStartRange.x),
                d2 = x.invert(focusStartRange.x + focusStartRange.dx),
                dd = data.slice(Math.max(0, pv.search.index(data, d1, function(d){
                    return d;
                }) - 1),
                pv.search.index(data, d2, function(d){ return d; }) + 1);
            fx.domain(d1, d2);
            fy.domain(y.domain());
            return dd;
        }).top(5 + labelOffset).height(h1);

        // Add X-axis
        focus.add(pv.Rule)
            .data(function() { return fx.ticks(); })
            .strokeStyle("#999")
            .left(fx)
            .bottom(0)
            .anchor("bottom").add(pv.Label)
            .text(fx.tickFormat);

        // Add Y-axis
        focus.add(pv.Rule)
            .data(y.ticks())
            .strokeStyle("#999")
            .bottom(fy)
          .anchor("left").add(pv.Label)
            .text(function(y) { return roundNumber(y);});

        var addLine = function(_data, lineNr) {
            focus.add(pv.Line)
            .data(_data)
            .strokeStyle(function(d) { return c(lineNr);})
            .bottom(function(d) {return fy(d);} )
            .left(function() {return fx(this.index);});
        };

        if (data && $.isArray(data[0])) {
            var i = 0;
            for (i = 0; i < data.length; i++) {
                d = data[i];
                addLine(d, i);
            }
        } else {
            addLine(data);
        }

        // Context panel
        var context = vis.add(pv.Panel)
            .bottom(0)
            .height(h2);

        /* X-axis ticks. */
        context.add(pv.Rule)
            .data(x.ticks())
            .left(x)
            .strokeStyle("#eee")
            .anchor("bottom")
            .add(pv.Label)
            .text(function(t) { return t; });

        /* Y-axis ticks. */
        context.add(pv.Rule).bottom(0);

        var addContextLine = function(_data, lineNr) {
            context.add(pv.Line)
                .data(_data)
                .strokeStyle(function(d) { return c(lineNr); })
                .bottom(function(d) {return y(d);} )
                .left(function() {return x(this.index);})
                .lineWidth(1);
        };

        // Context area chart.
        if (data && $.isArray(data[0])) {
            var i = 0;
            for (i = 0; i < data.length; i++) {
                d = data[i];
                addContextLine(d, i);
            }
        } else {
            addContextLine(data);
        }

        // The selectable, draggable focus region.
        context.add(pv.Panel)
            .data([focusStartRange])
            .cursor("crosshair")
            .events("all")
            .event("mousedown", pv.Behavior.select())
            .event("select", focus)
        .add(pv.Bar)
            .left(function(d){ return d.x; })
            .width(function(d){ return d.dx; })
            .fillStyle("rgba(0, 0, 0, .4)")
            .cursor("move")
            .event("mousedown", pv.Behavior.drag())
            .event("drag", focus);

       vis.render();

    };

    var dependencies = ["/static/lfw/js/libs/protovis-3.2/protovis-d3.2.js"];

    options.addDependency(cb, dependencies, true);
};
register(render);
