var render = function(options) {
    var TEMPLATE_NAME = 'plugin.protovis'; // this is only local I think
    var $this = $(this);
    var data_dict = $.parseJSON(options.body);
    var height = data_dict.height || 700;
    var width = data_dict.width || 700;
    var protovis_id = data_dict.protovis_id;
    var data = data_dict.data; // like this: [1, 1.2, 1.7, 1.5, .7, .5, .2]
    var horz_unit = data_dict.horz_unit; // should we name this like this?
    var horz_offset = data_dict.horz_offset;
    var vert_unit = data_dict.vert_unit;
    
    
    var cb = function(){
        $.template(TEMPLATE_NAME, '<div id=${protovis_id} style="height:${height}px;width:${width}px; "></div>');
        $.tmpl(TEMPLATE_NAME, {protovis_id:protovis_id, height:height, width:width}).appendTo($this);
        
        new pv.Panel()
            .canvas(protovis_id)
            .width(width)
            .height(height)
          .add(pv.Line)
            .data(data)
            .bottom(function(d) {return d * vert_unit;} )
            .left(function() {return this.index * horz_unit + horz_offset;})
          .root.render();
    };
    
    var dependencies = ["/static/lfw/js/libs/protovis-3.2/protovis-d3.2.js"];
    
    options.addDependency(cb, dependencies, true);
}
register(render);
