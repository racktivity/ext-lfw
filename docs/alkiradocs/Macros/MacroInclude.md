# Include Macro
Includes another page in the current page.


##Parameters

* **name**: Name of the page you which to include
* **space**: optional, name of the space where the page to include resides, if omitted, the current space is default.


##Example
Assuming we want to include the page [SubPage][] at the end of this page, we would add:

    [[include:name=SubPage]][[/include]]


##Sample

---

[[include:name=SubPage]][[/include]]

  [SubPage]: /sampleapp/#/alkiradocs/SubPage
