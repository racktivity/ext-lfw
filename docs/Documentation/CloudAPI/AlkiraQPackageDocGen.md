Alkira Q-Package Documentation Generator
========================================

The Alkira Q-Package documentation generator extension consists of 3 methods that contribute to the generating and publishing of the documentation:

* cloneMetaDataRepo
* generateDocumentation
* publishDocsToAlkira

Let's picture the following scenario parameters to see how the extension can be used:

__Metadata Repo:__ metadatarepo@incubaid.com  
__Repo Username:__ test\_user  
__Repo Password:__ test\_pass  

__Alkira Server:__ 127.0.0.1  
__Alkira Space:__ QP\_DOCS  
__Alkira page name:__ Q-Package Documentation  

__Destination to clone in:__ /my\_dest/files  
__Destination to generate documentation in:__ /my\_dest/docs  

Cloning the Metadata Repository
-------------------------------

The cloning method (cloneMetaDataRepo) is used to clone the metadata repository to certain destination on your local machine. It takes the following parameters:

* __repoUrl:__ The URL of the repository you want to clone.
* __repoUsername:__ The username to access the repository.
* __repoPassword:__ The password to access the repository.
* __localRepoPath:__ The destination path where you want the repository to get cloned to. If the path does not exist, it will be created.

In our case, we shall run it as follows:

    q.generator.qpackages.cloneMetaDataRepo('metadatarepo@incubaid.com', 'test_user', 'test_pass', '/my_dest/files')

Running this command will simply clone the metadata repository to '/my\_dest/files'.

Generating the Documentation
----------------------------

The generate documentation method (generateDocumentation) is used to generate Alkira documentation locally. This can be used in the case where you want to have the documentation on your machine for whatever purpose. It takes two parameters:

* clonedRepoPath
* outputPath

The cloned repository path is that path you chose to clone to using the previous method (cloneMetaDataRepo); while outputPath is where you want your Alkira documentation to be generated. In our case, we shall run the following command:

    q.generator.qpackages.generateDocumentation('/my_dest/files', '/my_dest/docs')

Running this command will generate Alkira formatted documentation in '/my\_test/docs'.

Publishing Documentation to Alkira
----------------------------------

The publish documentation to Alkira method (publishDocsToAlkira) is used to publish your generated documentation to an Alkira server, it takes the following parameters:

* __space:__ The name of the space on Alkira. If it doesn't exist, it gets created.
* __name:__ The name of the page where all the Q-Packages will be listed.
* __filesLocation:__ The lcoation where the documentation files where generated (using generateDocumentation).
* __hostname:__ The IP that the Alkira Client will use to get a connection and add the pages. Default is localhost.

In our case, we shall run it with the following parameters:

    q.generator.qpackages.publishDocsToAlkira('QP_DOC', 'Q-Package Documentation', '/my_test/docs', hostname='127.0.0.1')


