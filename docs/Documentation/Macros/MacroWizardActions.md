# Wizards Actions Macro

The Wiards Actions macro allows you to place a created wizard in an Alkira page.

## Parameters

None

## Example

Let us take a look at how we can add two very simple wizards to this page.

__Step 1:__

Create your wizard tasklets and place them under the following directory:

    /opt/qbase3/apps/applicationserver/services/wizard_engine/tasklets/

In our case, we created two wizard tasklets:

* hello\_wizard.py
* hello\_wizard\_name.py

__Step 2:__

Insure that the application server is running, then add the Wizards Actions macro to the page as follows:

    <div class="macro macro_wizardactions"></div>

__Step 3:__

Add the wizards themselves to the page. You can add them as a link, or a button or whatever suits your needs as long as it performs the javascript call:

    <a href="javascript:start('bla','hellowizard','172.19.6.163',success)" target='#'>Hello Wizard</a>
    <a href="javascript:start('bla','hellowizardname','172.19.6.163',success)" target='#'>Hello Wizard with Name</a>

Or:

    <button onclick="start('bla','hellowizard','172.19.6.163',success)">Hello Wizard</button>
    <button onclick="start('bla','hellowizardname','172.19.6.163',success)">Hello Wizard with Name</button>

You must insure that you add the Wizards Actions macro (Step 2) before adding the actual wizards to the page. This is because what the Wizards Actions macro actually does, is add all the dependencies needed by any wizard to run as well as add the CSS for it.

For example, your file should look like this:

    <div class="macro macro_wizardactions"></div>
    
    <a href="javascript:start('bla','hellowizard','172.19.6.163',success)" target='#'>Hello Wizard</a>
    <a href="javascript:start('bla','hellowizardname','172.19.6.163',success)" target='#'>Hello Wizard with Name</a>

__Note:__ You should change the IP in the examples above to the IP of your machine in order for them to work.

## Wizard Samples

<div class="macro macro_wizardactions"/>

* <a href="javascript:start('bla','hellowizard','172.19.6.163',success)" target='#'>Hello Wizard</a>
* <a href="javascript:start('bla','hellowizardname','172.19.6.163',success)" target='#'>Hello Wizard with Name</a>

Or:

<button onclick="start('bla','hellowizard','172.19.6.163',success)">Hello Wizard</button>
<button onclick="start('bla','hellowizardname','172.19.6.163',success)">Hello Wizard with Name</button>
