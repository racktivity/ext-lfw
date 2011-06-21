@metadata title=Page Validator Macro
@metadata tagstring=page validator link check macro

# Page Validator Macro
The `pagevalidator` macro creates a table displaying the state of all links and macros (broken/valid) found in a specific pages


##Parameters

* **spaces**: optional, comma separated list of all spaces that should be validated (`spaces:*` means all spaces)
* **pages**: optional, comma separated list of page names that has to be checked. if not specified all pages are checked
* **showvalid**: optional, if showvalid:false only invalid links/macros will be displayed
if neither "spaces" nor "pages" parameters are specified, default behavior is to check the current page and all child pages recursively


##Example
Assuming we want to show the invalid links/macros in the entire project

    [[pagevalidator]]
    spaces:*
    showvalid:false
    [[/pagevalidator]]

Assuming we want to show the all links/macros in the current page and its child pages
    [[pagevalidator]]
    [[/pagevalidator]]

Assuming we want to show the invalid links/macros of any page called Home or rest that is located in space API or space pylabs5

    [[pagevalidator]]
    spaces:api, pylabs5
    showvalid:Home,rest
    [[/pagevalidator]]
