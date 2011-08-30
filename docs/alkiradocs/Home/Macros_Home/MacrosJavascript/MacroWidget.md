@metadata title=Widget Macro
@metadata tagstring=macro alkira widget

#Widget Macro

The Widget macro allows you to add a widget to your page. In the body of the widget you put the macro that needs to be executed.
By using the widget macro, one can allow to hide/show a macro on his page.

##Parameters

Besides the macro, added in the body of the Widget macro, this macro accepts four different parameters (all optional)

* title: title for the used macro in the widget
* width: set the width of the macro
* height: set the height of the macro
* toggle: true/false, turn off the possibility of showing the widget (false). Default this parameter is true.


##Example

    [[widget:title=Note in a Widget, width=400, height=200, toggle=false]]
    [[note]]
    Show a note as a widget on a page
    [[/note]]
    [[/widget]]
	
##Sample

[[widget:title=Note in a Widget, width=400, height=200, toggle=false]]
	[[note]]
	Show a note as a widget on a page
	[[/note]]
[[/widget]]
	