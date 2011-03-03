[Documentation]: /#/Dev/Macros_HOWTO
[Macros]: /#/Dev/Macros

# Dev Space

This space is used to test the LFW!

## Macros

[Documentation][].


The [Macros][].

## Functionality Testing

As a first step I decided to test the LFW with some Arakoon pages. Here are a few points on my experience with the functionality.

### Code Blocks ###

Applying code blocks was fine, if code can be surrounded with a dashed box, or support script highlighting it would be a plus, but it is not essential.

_We already planned to create a code macro, with syntax highlighting etc_

### Links ###

I faced a small problem with reference style links. If you are using a reference style link for a local resource, it works fine; but if the link points to 'www.google.com' for example, it appends the current URL, in our case 'http://172.19.6.250/' to the link you're trying to reference.

Check [Google][g].

  [g]: http://www.google.com

For example 'www.google.com' turns into 'http://172.19.6.250/www.google.com'.

### Images ###

I currently can't test if images will have the same problem, because I get 'Permission Denied' whenever I try to 'scp' or 'wget' an image, if you can palce a test image for me in there it would be nice.

_You have to make sure that the webserver's user (e.g. qbase) has access to the file_:

    chown qbase:qbase filename


Other than that, the option of not being able to do anything than just add the images feels a bit restrictive. I don't have to be able to resize the image, but to insert it 'center' or 'right' would be handy.

_Maybe we can provide the aligning functionality using an image macro_

### Conclusion ###

Unless you want to create tables or insert diagrams at specific places, Markdown is quite easy to use, and gets the job done fast.
