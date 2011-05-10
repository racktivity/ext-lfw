[qpcreate]: http://confluence.incubaid.com/display/PYLABS/Creating+a+Q-Package
[codetasklet]: http://confluence.incubaid.com/display/PYLABS/Q-Package+Tasklets#codemanagement+Tasklet

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


##Publishing the Space and Pages

In order for any pages or spaces to be displayed, you need to run the `syncPortal` action in the Q-Shell:

    p.application.syncPortal('<pyapp name>')

This function makes all changes in the portal directories of your PyApp readily available. You only need to refresh your web browser to see the changes.


##Packaging Documentation
Adding the documentation to the Q-Package of your PyApp is identical to [creating a Q-Package][qpcreate]. Make sure that you add the new directories of your spaces in the [codemanagement][codetasklet] tasklet.