# Actions Macro

The Action macro allows you to add actions to a page.

When the Action macro is added to the page and called, it calls the 'WidgetService.py' with 'getWidgetConfig', this service is located under:

    /opt/qbase3/apps/applicationserver/services/widget_service

If you check the 'WidgetService.py' you will see that when called with 'getWidgetConfig', it executes the tasklet with tags 'widgit' and 'get'. This tasklet is the 'getwidgetconfig.py' tasklet and is located under:

    /opt/qbase3/apps/applicationserver/services/widget_service/tasklets/config

For testing purposes, this returns the position and name of the widget using 'console.log'. Of course you can write your own tasklets and actions that do a lot more than that.

## Parameters

None

## Example

To call the Action macro, we use:

    <div class="macro macro_actions"></div>

Adding a button to the page to execute an action:

    <form method="post" action="#/action/TestAction">
        <button type="submit" title="Test Action Button"></button>
    </form>

Where:

* TestAction: is the action name.
* Test Action Button: is the button title.

__Note:__ The alert message that appears is present in the code for testing purposes and proof of concept, it is not part of the tasklet.

### Button Sample:

<div class="macro macro_actions"/>

<form method="post" action="#/action/TestAction">
    <button type="submit" title="Test Action Button">Run test action!</button>
</form>