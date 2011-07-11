
function loadFileTree(divId, appname, root, contextMenuData)
{
    params = {
        "ui": {
            "select_limit": 1
        },
        "contextmenu": {
             "items" : contextMenuData
        },
        "json_data": {
            "ajax": {
                "url": "appserver/rest/ui/editor/listDirsInDir?appname=" + appname,
                "data": function(n) {
                    return {id: n.attr ? n.attr("id") : root};
                },
            "progressive_render" : true
            }
        },
        "themes" : {
           "theme" : "classic",
        },
        "plugins": ["themes", "json_data", "crrm", "ui"]
    }
    if (contextMenuData)
       params["plugins"].push("contextmenu");

    return $(divId).jstree(params);
}
