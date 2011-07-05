//@metadata wizard=protovis

var render = function(options) {
    var TEMPLATE_NAME = 'plugin.protovis'; // this is only local I think
    var $this = $(this);
    var data_dict = $.parseJSON(options.body);
    var height = data_dict.height || 300;
    var width = data_dict.width || 260;
    var protovis_id = data_dict.protovis_id;
    var data = data_dict.data; // like this: [1, 1.2, 1.7, 1.5, .7, .5, .2]
    var horz_unit = data_dict.horz_unit || 40; // should we name this like this?
    var horz_offset = data_dict.horz_offset || 0;
    var vert_unit = data_dict.vert_unit || 80;


    var cb = function() {
        var x = pv.Scale.linear(0, data.length).range(0, width);
        var y = pv.Scale.linear(data, function(d){ return d; }).range(0, height);

        $.template(TEMPLATE_NAME, '<div id=${protovis_id} style="height:${height}px;width:${width}px; "></div>');
        $.tmpl(TEMPLATE_NAME, {protovis_id:protovis_id, height:height, width:width}).appendTo($this);

        var vis = new pv.Panel()
            .canvas(protovis_id)
            .width(width - 20)
            .height(height - 25)
            .left(20)
            .bottom(25);

        // Add X-axis
        vis.add(pv.Rule)
            .data(x.ticks())
            .strokeStyle("#999")
            .left(x)
            .bottom(0)
            .height(5)
            .anchor("bottom").add(pv.Label)
            .text(x.tickFormat);

        // Add Y-axis
        vis.add(pv.Rule)
            .data(y.ticks())
            .strokeStyle("#999")
            .bottom(y)
          .anchor("left").add(pv.Label)
            .text(y.tickFormat);


        vis.add(pv.Line)
            .data(data)
            .bottom(function(d) {return y(d);} )
            .left(function() {return x(this.index);});

        vis.render();

    };

    var dependencies = ["/static/lfw/js/libs/protovis-3.2/protovis-d3.2.js"];

    options.addDependency(cb, dependencies, true);
};
register(render);
