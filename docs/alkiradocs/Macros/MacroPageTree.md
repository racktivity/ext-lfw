#Page Tree Macro

This macro shows a flexible hierarchical tree view.
It calls an lfw service which queries the database page schema and forms a recursive tree of parent-children relation


## Example
######If you want to display all pages that you have use this call:
        [[pagetree]][[/pagetree]]
######Or if you want to display the children of a certain page, then put the page's name in the body as follows:
        [[pagetree:root=Home]][[/pagetree]]

##Sample

[[pagetree]][[/pagetree]]

