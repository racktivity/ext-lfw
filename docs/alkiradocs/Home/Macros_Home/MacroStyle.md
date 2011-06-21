@metadata title=Style Macro
@metadata tagstring=style js javascript macro alkira


#Style Macro

The `style` macro allows you to add a specific style to your page. Instead of using the default style of your application, you can choose to apply a custom style per page.


##Parameters
* src: location to stylesheet file

Instead of referring to a stylesheet file, you can add css content to the markdown file. See the example below.


##Example

    [[style:src=http://bits.wikimedia.org/skins-1.5/monobook/main.css/]]
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque eu metus in mi vulputate convallis in vitae tellus. Mauris congue blandit felis id iaculis. Integer ut sodales ante. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Sed vitae tempus tortor. Fusce ut mi eget mi aliquet viverra. Donec vel pellentesque leo. Vestibulum eget ipsum ac mi condimentum suscipit eget non ante. Aenean ultricies arcu augue, ac commodo magna. Donec ultricies sapien vel diam volutpat at lacinia lectus pretium. Nullam tortor nunc, congue ut mollis vel, commodo nec elit. Curabitur viverra eros sed lorem euismod eget convallis tellus sodales. Nulla nisl magna, hendrerit id iaculis vitae, tincidunt et ligula. Duis vitae leo risus, ornare semper enim.

or stylesheet included in the markdown file:

    [[style]]
    body
    {
    background-color:#d0e4fe;
    }
    h1
    {
    color:orange;
    text-align:center;
    }
    p
    {
    font-family:"Times New Roman";
    font-size:20px;
    }
    [[/style]]

##Sample

This page uses the style of the first example.

[[style:src=http://bits.wikimedia.org/skins-1.5/monobook/main.css/]]
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque eu metus in mi vulputate convallis in vitae tellus. Mauris congue blandit felis id iaculis. Integer ut sodales ante. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Sed vitae tempus tortor. Fusce ut mi eget mi aliquet viverra. Donec vel pellentesque leo. Vestibulum eget ipsum ac mi condimentum suscipit eget non ante. Aenean ultricies arcu augue, ac commodo magna. Donec ultricies sapien vel diam volutpat at lacinia lectus pretium. Nullam tortor nunc, congue ut mollis vel, commodo nec elit. Curabitur viverra eros sed lorem euismod eget convallis tellus sodales. Nulla nisl magna, hendrerit id iaculis vitae, tincidunt et ligula. Duis vitae leo risus, ornare semper enim.
