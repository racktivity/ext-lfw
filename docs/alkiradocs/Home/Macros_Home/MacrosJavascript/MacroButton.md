@metadata title=Button Macro
@metadata tagstring=macro alkira button

[target]: http://www.w3schools.com/tags/att_a_target.asp
[fam]: http://www.famfamfam.com/lab/icons/silk/

#Button Macro
The Button macro allows you to add a button to your page which executes some javascript code.


##Parameters
The macro accepts the following parameters:

* href: link to a page
* click: javascript code that is executed when clicking the button
* name: name that appears on the button
* title: title of the button, appears when you hover over the button
* target: [target][] of the link
* icon: change the default icon of the button


##Example

    [[button:href=#/alkiradocs/MacroButton, click=alert("This is Incubaid"), name=Button, title=Title, target=_self /]]
    
    
##Sample

[[button:href=#/alkiradocs/MacroButton, click=alert("This is Incubaid"), name=Button, title=Title, target=_self/]] 


##How to Modify the Button Icon
Instead of using the default button icon as in the example above, one can choose his own icon. In this example we use a smiley icon (emoticon_smile.png, taken from [www.famfamfam.com][fam]), that replaces the caret (^) sign.
To do so, you have to add an icon to your system. The location of the icon in PyLabs is `/opt/qbase5/www/lfw/img`. This directory already contains a set of graphics. For maintenance reasons it is recommended to create a directory, for example `icons` in which you store the icons.

To make the icon available, you have to add a class to `theme.css` of your application. This file is located in `/opt/qbase5/www/lfw/css`.
To add class add the following line, provided that the icon, `emoticon_smile.png` is stored in `/opt/qbase5/www/lfw/img/icons`:

    .ui-state-default .<classname> {background-image: url("<link to icon>")}
    
where:

* <classname>: class name that you can use for the icon parameter of your button
* <link to icon>: link to the name of the icon, relative from `/opt/qbase5/www/lfw/css`

For example:
        
     .ui-state-default .emoticon-smile {background-image: url("../img/icons/emoticon_smile.png")}

For each icon that you want to use in your application, you have to create a new class. 

Define a button with a custom icon as follows:

    [[button:href=#/alkiradocs/MacroButton, click=alert("This is Incubaid"), name=Button, title=Title, target=_self, icon=<class name> /]]
    
for example:

    [[button:href=#/alkiradocs/MacroButton, click=alert("This is Incubaid"), name=Button, title=Title, target=_self, icon=emoticon-smile /]]
    
This is then the result:

[[button:href=#/Test/button, click=alert("This is Incubaid"), name=Button, title=Title, target=_self, icon=emoticon-smile /]]        