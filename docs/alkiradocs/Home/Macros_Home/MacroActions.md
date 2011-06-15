#Actions Macro

The Actions macro allows users to create a button that performs a certain action.   
The button information is located in a tasklet that gets executed by the generic service.

##Parameters

__None.__

##Action Tasklets

The tasklets are located under:

    /opt/qbase5/pyapps/sampleapp/impl/portal/pylabsmacro/actions/

Currently we have a sample tasklet called "test1.py" which contains the information of two buttons.   
Below is the tasklet code:

    __author__ = "incubaid"


    def main(q, i, params, tags):

        l ={"action": [
            {"name": "Print", "description": "Print this page", "uri": "javascript:print();", "target": "", "icon": "ui-icon-print"},
            {"name": "Google", "description": "Go To Google", "uri": "http://www.google.com", "target": "_blank", "icon": "ui-icon-link"}
        ]}

        params['result'] = l

    def match(q, i, params, tags):
        return True

When defining a button in a tasklet, as shown in the code above, it should contain the following parameters:

* __name:__ is the name that will appear on the button.
* __description:__ is the help text that will be displayed when you hover on the button.
* __uri:__ the action call; for example: "http://www.google.com" or "javascript:print();".
* __target:__ specifies where to open the linked document.
* __icon:__ is the icon that will be given to the button.

##Example

To call the Action macro, we use:

    [[actions]][[/actions]]

Below is the macro output:

[[actions]][[/actions]]


