@metadata title=Metadata
@metadata order=20
@metadata tagstring=metadata title order tagstring


[children]: #/alkiradocs/MacroChildren
[pagetree]: #/alkiradocs/MacroPageTree
[spaceandpage]: #/alkiradocs/SpacesAndPages



#Metadata
When you deploy your documentation, Alkira shows the pages in a random order. This results most of the time in an illogical order of spaces and pages.

By adding metadata to your pages, it is possible to order your spaces and pages.


##Title
The file names of your pages are most of the times kept as concise as possible. These file names are used in some of the macros, used to help the user browsing through the different spaces.
This may result in very hard to look up pages.

By using the metadata `title` you can apply an alternative name for your page. This alternative title is then used in the different Alkira macros, such as the [children][] and [pagetree][] macros. 

Usage:

At the top of your markdown file, add the following line:

	@metadata title=<your title here>

for example:

	@metadata title=This is an alternative title
	

##Order
To set a page order, use the metadata `order` where the lowest value has the highest priority. 
In case of child pages, the order of the child pages is independent from the parent page. As mentioned [earlier][spaceandpage], a child page is created by creating a subdirectory which contains a file with the same name as the subdirectory.

Usage:

At the top of your markdown file, add the following line:

	@metadata order=<number>
	
for example:

	@metadata order=10
		

Take the following example:

    ~/alkiradocs/Home
    |-- Home.md
    |-- Child1
    |   |-- Child1.md (child page of Home)
    |   |-- Child11.md (child page of Home)
    |   |-- Child12
    |   |   |-- Child12.md (child page of Child1)
    |   |   `-- Child121.md (child page of Child12)
    |   `-- Child13.md (child page of Child1)
    |-- Child2.md (child page of Home)
    `-- Child3
        |-- Child3.md (child page of Home)
        |-- Child31.md (child page of Child3)
        `-- Child32
            |-- Child32.md (child page of Child3)
            |-- Child33.md (child page of Child32)
            `-- Child34.md (child page of Child32)
	
Child1.md, child2.md, and Child3.md are all child pages from the Home page. Suppose that you want the following order in your space:

	Child3
	Child1
	Child2

Then Child3 may have order 10, Child1 order 20, and Child2 order 30.

As you can notice, Child1 and Child3 have on their turn child pages. The order of these child pages is completely independent from their parent pages.
This means that for example child page Child11 can also have order 10.


##Space Order
Just like page you can order your space too, except that you can only define the space order on the `Home.md` file of a space.

Usage:

	@metadata spaceorder=<number>
	
for example:

	@metadata spaceorder=10
	

##Tags and Strings		
To improve the search for information, you can add tags and labels to your page. 
Labels and tags have the same function, but labels are just keywords, while tags are key/value pairs.

Usage:

	@metadata tagstring=label1 label2 tag1:value1
	
As you can see the labels and tags are _not_ comma separated.