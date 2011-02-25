## Code Macro

The code macro can be used to display code on a page.
Syntax language is detected automatically and highligted accordingly.

### Parameters

The body of the macro is the code which should be highlighted.

### Examples

    <div class="macro macro_code">
        class MyClass(object):
            def __init__(self):
                # Do some init
    </div>

---
<div class="macro macro_code">
class MyClass(object):
	def __init__(self):
		# Do some init
</div>
---
