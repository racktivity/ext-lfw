@metadata title=Generating Documentation
@metadata order=60


#Alkira Q-Package Documentation Generator

The Alkira Q-Package documentation generator extension consists of three methods that contribute to the generation and publication of the documentation:

* cloneMetaDataRepo
* generateDocumentation
* publishDocsToAlkira

Assume the following settings to see how the extension can be used:

__Metadata Repo:__ metadatarepo@incubaid.com  
__Repo Username:__ test\_user  
__Repo Password:__ test\_pass  

__Alkira Server:__ 127.0.0.1  
__Alkira Space:__ QP\_DOCS  
__Alkira page name:__ Q-Package Documentation  

__Destination to clone in:__ /my\_dest/files  
__Destination to generate documentation in:__ /my\_dest/docs  


##Cloning the Metadata Repository

The cloning method (cloneMetaDataRepo) is used to clone the metadata repository to certain destination on your local machine. It takes the following arguments:

* __repoUrl:__ The URL of the repository you want to clone.
* __repoUsername:__ The username to access the repository.
* __repoPassword:__ The password to access the repository.
* __localRepoPath:__ The destination path where you want the repository to get cloned to. If the path does not exist, it will be created.

With the given settings, run the command as follows:

    q.generator.qpackages.cloneMetaDataRepo('metadatarepo@incubaid.com', 'test_user', 'test_pass', '/my_dest/files')

Running this command will simply clone the metadata repository to `/my_dest/files`.


##Generating the Documentation

The generate documentation method (`generateDocumentation`) is used to generate Alkira documentation locally, for example in case you want to quickly have a look at the layout of the documentation. 
The method takes two arguments:

* clonedRepoPath
* outputPath

The `clonedRepoPath` is the path you chose to clone when using the cloneMetaDataRepo method; while `outputPath` is where you want your Alkira documentation to be generated. 
With the given settings, run the command as follows:

    q.generator.qpackages.generateDocumentation('/my_dest/files', '/my_dest/docs')

Running this command will generate Alkira formatted documentation in '/my\_test/docs'.


##Publishing Documentation to Alkira
To publish your documentation in Alkira, use the `publishDocsToAlkira` method. This method takes the following arguments:

* __space:__ The name of the space on Alkira. If it does not exist, it is automatically created.
* __name:__ The name of the page where all the Q-Packages will be listed.
* __filesLocation:__ The location where the documentation files were generated (using generateDocumentation).
* __hostname:__ The IP that the Alkira Client will use to get a connection and add the pages. Default is localhost.

With the given settings, run the command with the following arguments:

    q.generator.qpackages.publishDocsToAlkira('QP_DOC', 'Q-Package Documentation', '/my_test/docs', hostname='127.0.0.1')
