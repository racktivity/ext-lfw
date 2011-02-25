## Generic Macro

A generic macro which renders content based on the pylabs tags defined in the body of the macro and the context of the page

### Parameters

*   *tagstring* 
*   The body of the macro should be a list of space separated tags and labes as defined by the Pylabs Tag format.

### Examples

    <div class="macro macro_generic">debug tagkey:tagvalue label sample</div>

---
<div class="macro macro_generic">debug tagkey:tagvalue label</div>
---

    <div class="macro macro_generic">a:b demo</div>

---
<div class="macro macro_generic">a:b demo</div>
---

