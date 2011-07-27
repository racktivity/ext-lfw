
(function($){
    $.fn.lock = function(name, handler){
        return this.each(function(){
            var $this = $(this);
            var ldata = $this.data("_lock");
            if (!ldata){
                ldata = {};
                $this.data("_lock", ldata);
            }
            
            if (!(name in ldata)){
                ldata[name] = {h: [], f: false};
            }
            
            var l = ldata[name];
            
            if (handler !== undefined && $.isFunction(handler)){
                l.h.push(handler);
            } else {
                l.f = true;
            }
            
            if (l.f) {
                $.each(l.h, function(i, v){
                    v();
                });
            }
            
            $this.data("_lock", ldata);
        });
    };
})(jQuery);
