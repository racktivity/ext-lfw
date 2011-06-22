var render = function(options) {
    var TEMPLATE_NAME = 'plugin.protovis'; // this is only local I think
    var $this = $(this);
    var data_dict = $.parseJSON(options.body);
    var height = data_dict.height || 400;
    var width = data_dict.width || 400;
    var protovis_id = data_dict.protovis_id;
    var data = data_dict.data; // like this: [1, 1.2, 1.7, 1.5, .7, .5, .2]
    var horz_unit = data_dict.horz_unit; // should we name this like this?
    var horz_offset = data_dict.horz_offset;
    var vert_unit = data_dict.vert_unit;
    
    
    var cb = function(){
        var x = null;
        var y = null;
        
        $.template(TEMPLATE_NAME, '<div id=${protovis_id} style="height:${height}px;width:${width}px; "></div>');
        $.tmpl(TEMPLATE_NAME, {protovis_id:protovis_id, height:height, width:width}).appendTo($this);
        
        // make scales if provided
        if (data_dict.x_scale) {
            x = pv.Scale.linear(0, data_dict.x_scale).range(0, width);
        }
        
        if (data_dict.y_scale) {
            y = pv.Scale.linear(0, data_dict.y_scale).range(0, height);
        }
        
        var vis = new pv.Panel()
            .canvas(protovis_id)
            .width(width)
            .height(height)
        
        vis.add(pv.Line)
            .data(data)
            .bottom(function(d) {return d * vert_unit;} )
            .left(function() {return this.index * horz_unit + horz_offset;});
        
        // render scales if provided
        // !!!! note the grid shows on Chrome but not on Firefox
        // the scales labels don't show on either
        if (x) {
            vis.add(pv.Rule)
                .data(x.ticks())
                .strokeStyle("#eee")
                .left(x)
              .anchor("bottom").add(pv.Label)
                .text(x.tickFormat);
        }
        
        if (y) {
            vis.add(pv.Rule)
                .data(y.ticks())
                .strokeStyle("#eee")
                .bottom(y)
              .anchor("left").add(pv.Label)
                .text(y.tickFormat);
        }
        
        
        vis.root.render();
        
    };
    
    var dependencies = ["/static/lfw/js/libs/protovis-3.2/protovis-d3.2.js"];
    
    options.addDependency(cb, dependencies, true);
}
register(render);
