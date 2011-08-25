@metadata title=Code Macro
@metadata tagstring=macro alkira code

#Code Macro
The `code` macro is used to display source code on a page.
Syntax language is detected automatically and highlighted accordingly.


##Parameters

The body of the macro is the code which should be highlighted.


##Example
Assume that you want to highlight the following code:

    class MyClass(object):
        def __init__(self):
            # Do some init

Use the code macro as follows:

    [[code]]
        class MyClass(object):
            def __init__(self):
                # Do some init
    [[/code]]


##Sample

[[code]]
class MyClass(object):
    def __init__(self):
        # Do some init
[[/code]]
