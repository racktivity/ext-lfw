# Code Macro

The code macro can be used to display code on a page.
Syntax language is detected automatically and highlighted accordingly.

## Parameters

The body of the macro is the code which should be highlighted.

## Example

Assuming we want to highlight the following code:

    class MyClass(object):
        def __init__(self):
            # Do some init

We use the code macro as follows:

    <div class="macro macro_code">
        class MyClass(object):
            def __init__(self):
                # Do some init
    </div>

## Sample

<div class="macro macro_code">
class MyClass(object):
	def __init__(self):
		# Do some init
</div>
