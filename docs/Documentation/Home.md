# Welcome to the Alkira Project

This page contains the Alkira documentation.

### What is Alkira?

* Alkira is a highly customizable wiki developed by Incubaid that uses the Markdown syntax.

### Why use it?

* Unlike most wikis, Alkira renders on the client side, not the server side. This makes it a lot faster due to the decreased load on the server.

- - -

## Markdown

Alkira uses the Markdown syntax, check the [Markdown](/#/Documentation/Markdown_Home) page for more details.

- - -

## Macros

We have written our own macros to be used with Alkira, check them out in the [Macro](/#/Documentation/Macros_Home) page.

- - -

## Managing Spaces & Pages

This section will walk you through creating a space, page and making them visable.

### How to Create a Space

Currently, you create a space by simply creating a directory under the following path:

    /opt/qbase3/var/qpackages4/files/pylabs.org/lfw/1.0/generic/docs/

For example, I created the 'Documentation' space by running the following command:

    mkdir /opt/qbase3/var/qpackages4/files/pylabs.org/lfw/1.0/generic/docs/Documentation

A space will not appear unless it contains a 'Home.md' page and the 'sync\_md\_to\_lfw.py' is run. Read the sections below for details on creating a page and how the script works.

### How to Create a Page

To create a page, create a Markdown file under the desired space folder.

In our a case, a 'Home.md' file was created. The content of this file is the page you are currently reading. Notice the URL (Documentation/Home).

### How to Synchronize your Files to the Server

In order for any pages or spaces to be displayed, you need to run the 'sync\_md\_to\_lfw.py' script. The script is located under:

    /opt/qbase3/var/qpackages4/files/pylabs.org/lfw/1.0/generic/scripts

This script goes through the directory:

    /opt/qbase3/var/qpackages4/files/pylabs.org/lfw/1.0/generic/docs/

and creates a space for every directory in there as long as it has a 'Home.md' file. Any folders under a space folder will not have a space created for them.

For example, this 'Documentation' space folders contains sub-folders such as 'Macros' and 'Markdown' but only a 'Documentation' space was created. This means that when you click on either the 'Macro' or 'Markdown' link, is takes you to 'Documentation/Markdown\_Home' not 'Documentation/Markdown/Markdown\_Home'.

- - -

## How Search Works

There are 3 searching fields:

* Title
* Labels
* Search

We shall go through how each search functions.

### Title

Searching in this field is done by matching the exact text you enter with page titles in the space.

For example, searching for 'Home' will take you to the home page of the Documentation space because it matches to the page named 'Home.md'. This means that the Title search will always return only one page as a result and take you to it. For further elaboration, if you search in the Title field for 'Hom', it will not display that a page named 'Home' exists, instead it will output that no page named 'Hom' exists.

### Labels

You can also search using tags and labels. Currently, when a page is created, we give it a default tag that is 'space:space\_name'; where space\_name is the name of the space that the page belongs to.

For example, since all our pages belong to the 'Documentation' space, searching for 'space:Documentation' will return all the pages in that space since they all were assigned that tag during creation.

__Note:__ The Label search field is comma seperated, which means you can seach for several tags and labels at the same time in order to narrow down your search results.

### Search

In this field, whatever you write will be searched for in all the pages in the space. For example, if you search for the word 'create', all the pages that contain that word will be displayed.
