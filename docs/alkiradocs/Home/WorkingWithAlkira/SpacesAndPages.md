@metadata title=Spaces and Pages
@metadata order=10
@metadata tagstring=space page manage child

[qpcreate]: #/Q-Packages/QPCreate
[codetasklet]: #/Q-Packages/CodeManagement
[child]: #/alkiradocs/Macros/MacroChildren
[admin]: #/alkiradocs/UserGroupMgmt
[alkira]: #/alkiradocs/WorkingWithAlkira
[spacemgmt]: #/alkiradocs/SpaceMgmt
[imgCreateSpace]: images/images50/md_images/newspace.png
[imgNewPage]: images/images50/md_images/newpage.png


#Managing Spaces and Pages
When you create an application, it is possible to add documentation for the application, or you can simply create an application that only contains documentation.
The documentation is created on the Alkira platform.
In this section, we explain how you can manage Alkira spaces and pages.


##Creating a Space
There are two ways to create spaces in Alkira:

* via the Alkira user interface of your PyApp
* command line on the server running Alkira


### Alkira User Interface
To be able to create a new space in Alkira, you need [administrative rights][admin]. 
To create a new space in your application:

1. Select the __Admin__ space of the PyApp.
2. Go to the __Spaces__ page. An overview of existing spaces appears.
3. Click __Create New Space__, a form appears to create a space.
![CreateSpace][imgCreateSpace]
4. Provide a name for the space and click __Create Space__. 
The new space appears in the list of spaces.

[[note]]
**Important**

Do not use white spaces in the name of your space.
[[/note]]

Use this section also to rename or remove spaces. See the [Space Management section][spacemgmt]


### Command Line
You create a space by simply creating a directory under the following path:

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
Similar to creating Alkira spaces, there exist two ways to create pages:

* via the Alkira user interface of your PyApp
* command line on the server running Alkira


###Alkira User Interface
To be able to create or update pages, you need [administrative rights][admin].
To create a new page in your application:

1. Select the space in which you want to add a page.
2. By default the Home page of the space is shown. Your new page will be a child page of the Home page. 
If your page must have another parent page, then first select the proper parent page before continuing. 
3. Click __New__. A form appears to create a new page.
![newpage][imgNewPage]
4. Fill out the _Name_ and _Title_ of your page. Leave _Type_ to 'Markup', _Tags_ are automatically added when saving your page.
	* __Name__: file name of your page
	* __Title__: name of the page that appears in pagetrees and lists of child pages
5. Create your page, see the [Working with Alkira][alkira] section.
6. Click __Save__. The page is added to Alkira.


###Command Line
To create a page, create a Markdown file in the desired space. A markdown file has always the `.md` extension.

In this case, a `Home.md` file is created in `/opt/qbase5/pyapps/<pyapp name>/portal/spaces/alkiradocs`. 


####Creating Child Pages
If you want to create a child page to a certain page, create a folder and inside that folder a `.md` file with the exact same name as the folder (case-sensitive). Possible other pages in that directory are also child pages.
There is no limitation in the number of levels


    ~/alkiradocs/
    |	Home.md
    `-- Home
	    |-- child1.md (child page of Home)
        |-- child1 
        |	|-- child11.md (child page of child1)
        |	|-- child12.md (child page of child1)
        |   |-- child12
        |	|   `-- child121.md (child page of child12) 
        |   `-- child13.md (child page of child1)
	    |-- child2.md (child page of Home)
	    |-- child3.md (child page of Home)
	    `-- child3    
	        |-- child31.md (child page of Child3)
	        `-- child32.md
	            |-- child32
	            	|-- child321.md (child page of child32)
	            	`-- child322.md (child page of child32)
        
In the given example you can clearly see the relationship between the different pages.

This way you can easily create a complete structure with parent/children relationships between your pages. See the [children macro][child] how you can use this structure inside a page.


##Publishing the Space and Pages

In order for any pages or spaces to be displayed, you need to run the `syncPortal` action in the Q-Shell:

    p.application.syncPortal('<pyapp name>')

This function makes all changes in the portal directories of your PyApp readily available. You only need to refresh your web browser to see the changes.


##Packaging Documentation
Adding the documentation to the Q-Package of your PyApp is identical to [creating a Q-Package][qpcreate]. Make sure that you add the new directories of your spaces in the [codemanagement][codetasklet] tasklet.