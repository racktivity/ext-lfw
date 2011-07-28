
(function($){
    $.fn.lock = function(name, handler) {
        return this.each(function(){
            var $this = $(this);
            var ldata = $this.data("_lock");
            
            if (!name) {
                $this.data("_lock", {});
                return;
            }
            
            if (!ldata){
                ldata = {};
                $this.data("_lock", ldata);
            }
            
            if (!(name in ldata)){
                ldata[name] = {h: $.noop, f: false};
            }
            
            var l = ldata[name];
            
            if (handler !== undefined && $.isFunction(handler)){
                l.h = handler;
            } else {
                l.f = true;
            }
            
            if (l.f && l.h !== $.noop) {
                l.h();
            }
            
            $this.data("_lock", ldata);
        });
    };
})(jQuery);
