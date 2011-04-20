#Managing Spaces and Pages
In this section, we explain how you can work with Alkira spaces and pages.


###Creating a Space

Currently, you create a space by simply creating a directory under the following path:

    /opt/qbase5/var/qpackages4/files/pylabs.org/lfw/1.0/generic/docs/

For example, create a space `Documentation` by running the following command:

    mkdir /opt/qbase5/var/qpackages4/files/pylabs.org/lfw/1.0/generic/docs/alkiradocs

The created space only appears when the directory contains a `Home.md` page and the `sync_md_to_lfw.py` is run. 
Read the sections below for details on creating a page and how the script works.


###Creating a Page

To create a page, create a Markdown file in the desired space. A markdown file has always the `.md` extension.

In this case, a 'Home.md' file is created in `/opt/qbase5/var/qpackages4/files/pylabs.org/lfw/1.0/generic/docs/alkiradocs`. 


###How to Synchronize your Files to the Server

In order for any pages or spaces to be displayed, you need to run the `sync_md_to_lfw.py` script. The script is located in:

    /opt/qbase5/var/qpackages4/files/pylabs.org/lfw/1.0/generic/scripts

This script analyzes the directory:

    /opt/qbase5/var/qpackages4/files/pylabs.org/lfw/1.0/generic/docs/

and creates a space for every directory in there as long as it has a `Home.md` file. Any folders under a space folder will not have a space created for them.

For example, the `Documentation` space folders contains sub-folders such as `Macros` and `Markdown` but only a `alkiradocs` space is created since only this directory contains the file `Home.md`. 
This means that when you follow either the `Macros` or `Markdown` link, you go to `alkiradocs/Markdown_Home` not `alkiradocs/Markdown/Markdown_Home`.