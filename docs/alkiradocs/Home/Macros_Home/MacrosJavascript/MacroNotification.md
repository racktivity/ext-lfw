@metadata title=Notification Macro
@metadata tagstring=macro alkira pageupdate notification

[[style:src=css/jmNotify.css/]]
[[script:src=js/libs/jquery.jmNotify.js/]]

#Macro Notification
The notification macro is used to show a notification when the page which you are currently looking at is updated.


## Parameters

* content: Content the notification should show when a new version of the current page comes available
* cssclass: CSS class that should be added to make the notification show (default customNotify)
* delay: Time the notification should be visible in milliseconds; -1 means infinity which is the default

## Example
    [[notification:content=This page is updated,delay=-1/]]


##Sample
See the notification on top of your browser.

[[notification:content=This page is updated,delay=-1/]]
