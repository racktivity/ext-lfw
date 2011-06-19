@metadata title=Pagetree Macro
@metadata tagstring=macro alkira pagetree tree page

#Page Tree Macro

The `pagetree` macro shows a flexible hierarchical tree view.
It calls an Alkira service which queries the database page schema and then forms a recursive tree of parent-children relation.


##Parameters
The `pagetree` macro can take the `root` parameter which indicates the root page from which the page tree must be built.


## Example

If you want to display all pages that you have use this call:
    
    [[pagetree]][[/pagetree]]


Or if you want to display the children of a certain page, then put the page's name in the body as follows:
    
    [[pagetree:root=Home]][[/pagetree]]
    
You can also show the pagetree of another space:

    [[pagetree:space=AnotherSpace]][[/pagetree]]    

##Sample

[[pagetree]][[/pagetree]]

