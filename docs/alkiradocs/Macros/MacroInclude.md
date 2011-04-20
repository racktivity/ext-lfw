# Include Macro
Includes another page in the current page.


##Parameters

* **name**: Name of the page you which to include
* **space**: optional, name of the space where the page to include resides, if omitted, the current space is default.


##Example
Assuming we want to include the page [SubPage][] at the end of this page, we would add:

    <div class="macro macro_include">{"name": "SubPage"}</div>


##Sample

---

<div class="macro macro_include">{"name": "SubPage"}</div>

  [SubPage]: /sampleapp/#/alkiradocs/SubPage
