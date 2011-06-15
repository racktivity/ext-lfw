[qpcreate]: http://confluence.incubaid.com/display/PYLABS/Creating+a+Q-Package
[codetasklet]: http://confluence.incubaid.com/display/PYLABS/Q-Package+Tasklets#codemanagement+Tasklet
[child]: /sampleapp/#/alkiradocs/Macros/MacroChildren

#Managing Spaces and Pages
When you create an application, it is possible to add documentation for the application, or you can simply create an application that only contains documentation.
The documentation is created on the Alkira platform.
In this section, we explain how you can manage Alkira spaces and pages.


##Creating a Space

Currently, you create a space by simply creating a directory under the following path:

    /opt/qbase5/pyapps/<pyapp name>/portal/spaces
    
For example, in the 'sampleapp' application there are four spaces, `alkiradocs`, `api`, `crm`, and `doc`:

* `/opt/qbase5/pyapps/sampleapp/portal/spaces/alkiradocs`
* `/opt/qbase5/pyapps/sampleapp/portal/spaces/api`
* `/opt/qbase5/pyapps/sampleapp/portal/spaces/crm`
* `/opt/qbase5/pyapps/sampleapp/portal/spaces/doc`
    

If you want to add a space to the 'sampleapp' application, create an extra directory, for example `mytest` by running the following command:

    mkdir /opt/qbase5/pyapps/sampleapp/portal/spaces/mytest

To make the new space available in your application, you must create the file `Home.md` in this directory and run the `syncPortal` action in the Q-Shell:

    p.application.syncPortal('<pyapp name>')
 

##Creating a Page

To create a page, create a Markdown file in the desired space. A markdown file has always the `.md` extension.

In this case, a 'Home.md' file is created in `/opt/qbase5/pyapps/<pyapp name>/portal/spaces/alkiradocs`. 


##Creating Child Pages
If you want to create a child page to a certain page, create a folder and inside that folder a `.md` file with the exact same name as the folder (case-sensitive). Possible other pages in that directory are also child pages.
There is no limitation in the number of levels


    ~/alkiradocs/Home
    |-- Home.md
    |-- Child1
    |   |-- Child1.md (child page of Home)
    |   |-- child11.md (child page of Home)
    |   |-- Child12
    |   |   |-- Child12.md (child page of Home)
    |   |   `-- child121.md (child page of Child12)
    |   `-- child13.md (child page of Home)
    |-- child2.md (child page of Home)
    `-- Child3
        |-- Child3.md (child page of Home)
        |-- child31.md (child page of Home)
        `-- Child32
            |-- Child32.md (child page of Home)
            |-- child33.md (child page of Child32)
            `-- child34.md (child page of Child32)
        
In the given example you can clearly see the relationship between the different pages.

This way you can easily create a complete structure with parent/children relationships between your pages. See the [children macro][child] how you can use this structure inside a page.


##Publishing the Space and Pages

In order for any pages or spaces to be displayed, you need to run the `syncPortal` action in the Q-Shell:

    p.application.syncPortal('<pyapp name>')

This function makes all changes in the portal directories of your PyApp readily available. You only need to refresh your web browser to see the changes.


##Packaging Documentation
Adding the documentation to the Q-Package of your PyApp is identical to [creating a Q-Package][qpcreate]. Make sure that you add the new directories of your spaces in the [codemanagement][codetasklet] tasklet.