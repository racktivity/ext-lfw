@metadata title=Alkira Macros
@metadata order=30
@metadata tagstring=macro alkira home

[howto]: /sampleapp/#/alkiradocs/Macros\_HOWTO
[pylabs]: /sampleapp/#/alkiradocs/MacrosPylabs
[js]: /sampleapp/#/alkiradocs/MacrosJavascript

#Alkira Macros

As we have mentioned, Alkira is highly customizable; this is due to the fact that you can develop your own macros, which are written in _JavaScript_.

There are two types of macros:

* __[PyLabs Macros][pylabs]__
* __[JavaScript Macros][js]__

## PyLabs Macros
PyLabs Macros render content based on the PyLabs tags defined in the body of the macro and the content of the page.
The content that this macro renders is a result of the execution of certain tasklets. 


## JavaScript Macros
JavaScript Macros, on the other hand, have to do with editing the page. These macros can have a wide range of usage, from highlighting code and showing a Google map, to adding a Wizard.
The macro files themselves (JavaScript files) are stored in `/opt/qbase5/www/lfw/js/macros` and must have unique names.

In this section you can find an overview of the available macros and how you can [create your own macro][howto].

##Overview of Existing Macros

[[include:name=Macros]][[/include]]