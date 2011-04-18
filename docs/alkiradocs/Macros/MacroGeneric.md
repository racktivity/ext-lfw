# Generic Macro

A generic macro which renders content based on the Pylabs tags defined in the body of the macro and the context of the page.

The content that this macro renders is a result of the execution of certain tasklets. These tasklets are present under:

    /opt/qbase5/apps/applicationserver/services/widget_service/tasklets/generic

Currently there are two test tasklets present under that directory:

* test1.py
* test2.py

When the Generic macro is called with 'debug' as one of the labels, test1.py gets executed. When the Generic macro is called with 'demo' as a label, test2.py gets executed.

We shall go through an example for a more detailed explanation.

## Parameters

* The body of the macro should be a list of space separated tags and labes as defined by the Pylabs Tag format.

## Example 1

The tasklet test1.py lists all the tags and labels in a page. As we have mentioned in explaining how the search functions, all the pages are created with default tags that are:

* space:space\_name
* page:page\_name

Where space\_name is the name of the space and page\_name is the name of the page. Sample 1 is the result of calling the Generic macro with debug as one of the labels; code is shown below:

    <div class="macro macro_generic">debug tagkey:tagvalue label sample</div>

### Sample 1

---
<div class="macro macro_generic">debug tagkey:tagvalue label</div>

## Example 2

The tasklet test2.py on the other hand, only prints out a default message. Sample 2 is the result of calling the Generic macro with 'demo' as a label; code is shown below:

    <div class="macro macro_generic">a:b demo</div>

### Sample 2

---
<div class="macro macro_generic">a:b demo</div>
