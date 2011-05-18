#Dashboard Macro
The `dashboard` macro allows you to add pages or other macros as widgets in your Alkira page.


##Parameters
The parameters of the Dashboard macro are the widgets you would like to include in the page. Take a look at the example.


##Example
Assume that you want to add the following widgets to your page:

First Column:

* Home page
* Actions

Second Column:

* Macros page
* Youtube macro

__Note:__ The youtube macro is for demo only and currently shows the Monty Python video.

##Code and Explanation

    [[dashboard]]
    {
      "columns": [
        {
          "order": 0,
          "widgets": [
            {"order": 0, "id": "widget1", "widgettype": "include", "title": "Widget 1", "params": {"name": "Macros_Home"}},
            {"order": 1, "id": "widget2", "widgettype": "actions", "title": "Actions", "config": {}}
          ]
        },
        {
          "order": 1,
          "widgets": [
            {"order": 0, "id": "widget3", "widgettype": "include", "title": "Widget 3", "params": {"name": "Macros"}},
            {"order": 1, "id": "widget4", "widgettype": "youtube", "title": "Monty Python", "config": {}}
          ]
        }
      ],
      "id": "dashboard1",
       "title": "My Dashboard"
    }
    [[/dashboard]]

There are three main sections:

* Columns
* ID
* Title


###Columns

This is where everything is mainly defined. For every column you want to add, you will have a section containing two variables:

* Order: a number that specifies in which column you want to add the widgets.
* Widgets: a list that contains the actual widgets you want to add, it has the following parameters:
    * __order:__ The position of the widget inside the previous column you chose before.
    * __id:__ An ID given to the widget.
    * __widgettype:__ Specifies which macro the widget will contain. You should write the macro name itself. For example, if you want the widget to include the Home page, then you set the widgit type to 'include'. If you want to display the youtube widgit, then you set it to 'youtube'.
    * __title:__ A title which is displayed in the title bar of the widget.
    * __config:__ If the macro you want to add uses the body as a parameter (for example, the [code macro][] or [include macro][]), then you write that body in the config parameter.
    * __params:__ The parameters you want to pass to the macro


###ID
This is a unique identifier for your dashboard.


###Title
This is the title that is displayed in the title bar of the dashboard.


##Sample

[[dashboard]]
{
    "columns": [
      {
        "order": 0,
        "widgets": [
          {"order": 0, "id": "widget1", "widgettype": "include", "title": "Widget 1", "params": {"name": "Macros_Home"}},
          {"order": 1, "id": "widget2", "widgettype": "actions", "title": "Actions", "config": {}}
        ]
      },
      {
        "order": 1,
        "widgets": [
          {"order": 0, "id": "widget3", "widgettype": "include", "title": "Widget 3", "params": {"name": "Macros"}},
          {"order": 1, "id": "widget4", "widgettype": "youtube", "title": "Monty Python"}
        ]
      }
    ], 
    "id": "dashboard1", 
    "title": "My Dashboard"
}
[[/dashboard]]

[code macro]: /sampleapp/#/alkiradocs/MacroCode
[include macro]: /sampleapp/#/alkiradocs/MacroInclude
