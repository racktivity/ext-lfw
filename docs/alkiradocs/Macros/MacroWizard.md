#Wizards Macro
The Wizards macro allows you to add a created [wizard](/sampleapp/#/doc/formwizardpractical) in an Alkira page.


## Parameters
* appserver: name of the application server that runs the wizard, by default the application server of the domain of your document
* title: title for your wizard, as it will appear in your document
* name: name of the wizard, must be the name of the directory in which the desired wizard is located
* type: type of element in your document, either _button_ (by default) or _link_
* appname: name of the application which contains the wizard, by default the application in which your document is included
* domain: name of the domain in the application, by default the domain is the space
* extra: the 'extra' params used in the wizards

The _title_ and _name_ parameters are required, all other parameters are optional.

## Example
Below you can find two examples of how you can add wizards into an Alkira page. The first is used as a button on your page, the latter is a link to another page in your browser.

    [[wizard:title=mywizard, name=customer_create, type=button, appname=sampleapp, domain=crm]][[/wizard]]
    [[wizard:title=anotherwizard, name=lead_create, type=button]][[/wizard]]

It is recommended to always fill out the parameter appname and domain, but it is not required.


##Wizard Samples

[[wizard:title=mywizard, name=customer_create, type=button, appname=sampleapp, domain=crm]][[/wizard]]

<br />

[[wizard:title=anotherwizard, name=lead_create, type=button, appname=sampleapp, domain=crm]][[/wizard]]
