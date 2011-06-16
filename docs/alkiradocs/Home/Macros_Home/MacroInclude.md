@metadata title=Include Macro
@metadata tagstring=macro alkira include


# Include Macro
The `include` macro includes the content of another page in the current page.


##Parameters

* **name**: Name of the page you which to include
* **space**: optional, name of the space where the page to include resides, if omitted, the current space is default.


##Example
Assuming we want to include the page [SubPage][] at the end of this page, we would add:

    [[include:name=SubPage]][[/include]]
    [[include:space=anotherSpace, name=SubPageOfAnotherSpace]][[/include]]
    
    


##Sample

[[include:name=SubPage]][[/include]]
