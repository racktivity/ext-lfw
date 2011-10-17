@metadata title=Notification Macro
@metadata tagstring=macro alkira pageupdate notification

[[style:src=css/jmNotify.css/]]
[[script:src=js/libs/jquery.jmNotify.js/]]

#Macro Notification
The notification macro is used to show a notification when the page which you are currently looking at is updated.


## Parameters

* content: Content the notification should show when a new version of the current page comes available
* cssclass: CSS class that should be added to make the notification show (default customNotify)
* delay: Time the notification should be visible in miliseconds -1 means inifinity which is the default

## Example
    [[notification:content=The current page is updated/]]


##Sample
<div id='notification' class='customNotify'>The current page is updated</div>
<button onclick="$('#notification').jmNotify()">test</button>
