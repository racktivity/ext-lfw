Alkira Client
=============

The Alkira client is an extension that was built to ease the interaction with the Alkira database/server. Instead of having to access the database files manually in order to, for example, create, update or remove a page; a set of methods were implemented to do this for you. This tutorial will walk you through using the Alkira client.

For demonstration purposes, let's assume we have the following in our Alkira server:

* Spaces: Dev, Docs
* Pages: Dev\_Home, Docs\_Home

Getting a Client Connecton
--------------------------

To access all the methods the client offers, you need to get a client connection, this is done by running the following command:  

    alkiraclient = q.clients.alkira.getClient(hostname='127.0.0.1')

__Note:__ The 'hostname' can be any IP that contains an Alkira Database.

Client Methods
--------------

Now that you have a client object, you can perform the tasks below.

### Listing the Current Spaces
##### alkiraclient.listSpaces()

This method takes no parameters, and lists all the spaces you have on the server.

__Example:__  

    In [1]: alkiraclient.listSpaces()
    Out[1]: ['Dev', 'Docs']

### Listing the Pages in a Space
##### alkiraclient.listPages(space)

This method takes the name of a space as a parameter, and returns all the pages in it.

__Example:__  

    In [1]: alkiraclient.listPages('Docs')
    Out[1]: ['Docs_Home']

###Checking if a Page Exists
##### alkiraclient.pageExists(space, name)

This method checks whether a certain page exists in a certain space or not. It takes the space name and page name as parameters.

__Example:__  

    In [1]: alkiraclient.pageExists('Docs', 'Docs_Home')
    Out[1]: True
    
    In [1]: alkiraclient.pageExists('Docs', 'Docs_Other')
    Out[1]: False

### Getting a Page Object
##### alkiraclient.getPage(space, name)

This method takes the space name and page name as parameters and returns a page object. Can be used to quickly check certain parameters of a page, such as tags or category.

__Example:__  

    In [1]: docshome = alkiraclient.getPage('Docs', 'Docs_Home')

Now you can check all the page properties:  

    In [1]: docshome.
    docshome.OSIS_MODEL_INFO  docshome.content          docshome.deserialize(     docshome.name             docshome.serialize(       docshome.tags             
    docshome.category         docshome.creationdate     docshome.guid             docshome.parent           docshome.space            docshome.version     

### Creating a New Page
##### alkiraclient.createPage(space, name, content, tagsList=[], category='portal', parent=None, contentIsFilePath=False)

This method is used to create a new page, it takes the following parameters:  

* space: The name of the space you want to add the page to.
* name: The name you want to give to the page.
* content: The content of the page. This can also be a file path; in this case you should set contentIsFilePath=True.
* tagsList: A list containing all the tags you want to add to the page.
* category: The category of the page. Default is 'portal'.
* parent: If you want this to become a child page, add the name of the parent page to this parameter. Default is None.
* contentIsFilePath: If the content you gave is a file path, set this value to True. Default is False.

__Example:__  

    In [1]: alkiraclient.createPage('Docs', 'Docs_Other', 'This is a test page.', parent='Docs_Home')

This creates a page called 'Docs\_Other' with content 'This is a test page' in the space 'Docs'.  
The page is also a child page of 'Docs\_Home'.

If on the other hand, you have a file called 'test\_info.md' under the directory '/my\_files' and you want the page you're creating to display/contain the contents of that file, you should call 'createPage' as follows:  

    In [1]: alkiraclient.createPage('Docs', 'Docs_Other', '/my_files/test_info.md', parent='Docs_Home', contentIsFilePath=True)

### Updating an Existing Page
##### alkiraclient.updatePage(old\_space, old\_name, space=None, name=None, tagsList=None, content=None, parent=None, category=None, contentIsFilePath=False)

The 'updatePage' method works exactly like the 'createPage' method, but instead of creating a new page, it gets the existing page from the database and then checks which parameters you have specified values for and updates them.

__Example:__  

If you want 'Docs\_Other' to contain 'Adjusted test page.' instead of 'This is a test page.' then you would call 'updatePage' as follows:  

    In [1]: alkiraclient.updatePage('Docs', 'Docs_Other', content='Adjusted test page.')

### Deleting a Page
##### alkiraclient.deletePage(space, name)

This method is used to delete a single page. It takes the space name and page name as parameters. If the page has any children pages, these links will be broken.

__Example:__  

If you want to delete the page 'Docs\_Other' you would perform:  

    In [1]: alkiraclient.deletePage('Docs', 'Docs_Other')

### Deleting a Page and Children
##### alkiraclient.deletePageAndChildren(space, name)

This method works in the same way as 'deletePage', except that is checks if the page has children pages. If yes, it deletes the children pages and in turn, checks if they had children pages, if yes, deletes them and so on.

__Example:__  

If you want to delete the page 'Docs\_Home' and any children it has, in our case 'Docs\_Other', you should use:  

    In [1]: alkiraclient.deletePageAndChildren('Docs', 'Docs_Home')


