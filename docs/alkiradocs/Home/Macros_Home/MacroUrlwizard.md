@metadata title=URL wizard Macro
@metadata tagstring=macro alkira wizard urlwizard

[wizardpage1]: urlwizardPage?title=mywizard&name=customer_create&domain=crm
[wizardpage2]: urlwizardPage?title=anotherwizard&name=lead_create&type=button&domain=crm

#Urlwizard Macro
The `urlwizard` macro creates a wizard that opens immediately and


##Parameters
The macro does not use parameters nor a body.
The macro gets its information from the URL: Possible url params are:

* __appserver__: name of the application server that runs the wizard, by default the application server of the domain of your document
* __title__: title for your wizard, as it will appear in your document
* __name__: name of the wizard, must be the name of the directory in which the desired wizard is located
* __appname__: name of the application which contains the wizard, by default the application in which your document is included
* __domain__: name of the domain in the application, by default the domain is the space
* __extra__: the 'extra' params used in the wizards

The _title_ and _name_ parameters are required, all other parameters are optional.


##Macro usage
    [[urlwizard/]]

##Example URLs
* [wizardpage1]
* [wizardpage2]
