@metadata title=Using Macros
@metadata order=15
@metadata tagstring=macro use usage

[createpage]: #/alkiradocs/SpacesAndPages
[rgraph]: #/alkiradocs/MacroRgraph
[REST]: http://en.wikipedia.org/wiki/Representational_State_Transfer
[appserver]: /pylabsdoc/#/Components/AppServer

#Using Macros in Documentation

When you [create a page][createpage], you can add macros to for example to add a graphic or information block.

To include a macro on a page, you have to apply this structure:

    [[name_of_macro]][[/name_of_macro]]

Each macro has its own properties: some macros need data, some need configuration, and some macros work without any additional information.


##Macro Configuration

Configuration parameters of a macro are added in the opening tag of the macro:

    [[name_of_macro: param1=foo, param2=480]][[/name_of_macro]] 
    

##Macro Data

If a macro needs data, for example to build a graph, then this must be provided in the body of the macro, for example see the [RGraph Macro][rgraph].

If the macro doesn't have a body, then you can use the short notation of the macro, similar to the short notation of an html tag:

    [[name_of_macro/]]
    
or

     [[name_of_macro: param1=foo, param2=480 /]]
     

##REST Calls
A parameter of a macro can also be a [REST call][rest] to a [PyApps' application server service][appserver]. This allows you to execute a service inside your macro.

To make a REST call in a macro use the following structure:

    [[name_of_macro: call=appserver/rest/link/to/appserver/service]][[/name_of_macro]]
    
for example:

    [[note: call=appserver/rest/ui/portal/listSpaces]][[/note]]
    
results in:

[[note: call=appserver/rest/ui/portal/listSpaces]][[/note]]
