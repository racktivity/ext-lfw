## Include Macro

Includes another page in the current page.

### Parameters

*   *name*

    Name of the page you which to include

*   *space (optional)*

    Name of the space where the page to include resides.
    If ommited, the current space is default.

### Examples

This will include the page '[SubPage][]':

    <div class="macro macro_include">{"name": "SubPage"}</div>

---
<div class="macro macro_include">{"name": "SubPage"}</div>
---

  [SubPage]: /#/Dev/SubPage