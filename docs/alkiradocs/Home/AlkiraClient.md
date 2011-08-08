@metadata title=Alkira Client
@metadata order=40
@metadata tagstring=client qshell alkira


#Alkira Client
The Alkira client is an extension for interaction with the Alkira database/server. Instead of having to access the database files manually, a set of methods are implemented to in order to, for example create, update, or remove a page. This section gives you an overview of the Alkira client functions.

In this document, we assume that we have the following data in our Alkira server:

* Spaces: Dev, Docs
* Pages: Dev\_Home, Docs\_Home


##Getting a Client Connection

To access all the methods the client offers, you need to get a client connection. You can establish a connection by running the following command:  

    alkiraclient = q.clients.alkira.getClient(hostname='127.0.0.1')

__Note:__ The 'hostname' can be any IP that contains an Alkira Database.


##Client Methods
Now that you have a client object, you can perform the tasks below.


###Listing the Current Spaces
    
    alkiraclient.listSpaces()

This method takes no parameters, and lists all the spaces you have on the server.

__Example:__  

    In [1]: alkiraclient.listSpaces()
    Out[1]: ['Dev', 'Docs']


###Listing the Pages in a Space

    alkiraclient.listPages(space)

This method takes the name of a space as a parameter, and returns all the pages in it.

__Example:__  

    In [1]: alkiraclient.listPages('Docs')
    Out[1]: ['Docs_Home']


###Checking if a Page Exists

    alkiraclient.pageExists(space, name)

This method checks whether a certain page exists in a certain space or not. It takes the space name and page name as parameters.

__Example:__  

    In [1]: alkiraclient.pageExists('Docs', 'Docs_Home')
    Out[1]: True
    
    In [1]: alkiraclient.pageExists('Docs', 'Docs_Other')
    Out[1]: False


###Getting a Page Object

    alkiraclient.getPage(space, name)

This method takes the space name and page name as parameters and returns a page object. Can be used to quickly check certain parameters of a page, such as tags or category.

__Example:__  

    In [1]: docshome = alkiraclient.getPage('Docs', 'Docs_Home')

Now you can check all the page properties:  

    In [1]: docshome.
    docshome.OSIS_MODEL_INFO  docshome.content          docshome.deserialize(     docshome.name             docshome.serialize(       docshome.tags             
    docshome.category         docshome.creationdate     docshome.guid             docshome.parent           docshome.space            docshome.version     


###Creating a New Page

    alkiraclient.createPage(space, name, content, tagsList=[], category='portal', parent=None, contentIsFilePath=False)

This method is used to create a new page, it takes the following parameters:  

* space: the name of the space you want to add the page to.
* name: the name you want to give to the page.
* content: the content of the page. This can also be a file path; in this case you should set `contentIsFilePath=True`.
* tagsList: a list containing all the tags you want to add to the page.
* category: the category of the page. By default the category is 'portal'.
* parent: if you want this to become a child page, add the name of the parent page to this parameter. The parent is by default `None`.
* contentIsFilePath: if the content you gave is a file path, set this value to `True`. This argument is by default `False`.

__Example:__  

    In [1]: alkiraclient.createPage('Docs', 'Docs_Other', 'This is a test page.', parent='Docs_Home')

This creates a page called `Docs_Other` with content 'This is a test page' in the space `Docs`.  
The page is also a child page of `Docs_Home`.

It is also possible to include the content of one page in another page. Assume that you have a file called `test_info.md` in the directory `/my_files`. If you want to display the contents of that file in the page `Docs_Other`, use the `createPage` as follows:  

    In [1]: alkiraclient.createPage('Docs', 'Docs_Other', '/my_files/test_info.md', parent='Docs_Home', contentIsFilePath=True)


###Updating an Existing Page

    alkiraclient.updatePage(old_space, old_name, space=None, name=None, tagsList=None, content=None, parent=None, category=None, contentIsFilePath=False)

The `updatePage` method is similar to the `createPage` method, but instead of creating a new page, `updatePage` gets the existing page from the database and updates the values of the page properties.

__Example:__  

If you want `Docs_Other` to contain 'Adjusted test page.' instead of 'This is a test page.' then you would call `updatePage` as follows:  

    In [1]: alkiraclient.updatePage('Docs', 'Docs_Other', content='Adjusted test page.')


###Deleting a Page

    alkiraclient.deletePage(space, name)

This method is used to delete a single page. It takes the space name and page name as parameters. If the page has any child pages, these links will be broken.

__Example:__  

If you want to delete the page `Docs_Other`:  

    In [1]: alkiraclient.deletePage('Docs', 'Docs_Other')


###Deleting a Page and Children

    alkiraclient.deletePageAndChildren(space, name)

The `deletePageAndChildren` method is similar to the `deletePage` method, but now checks if the page has child pages. The parent and child pages are deleted in a recursive way.

__Example:__  

If you want to delete the page `Docs_Home` and any children it has, in our case `Docs_Other`, you should use:  

    In [1]: alkiraclient.deletePageAndChildren('Docs', 'Docs_Home')


