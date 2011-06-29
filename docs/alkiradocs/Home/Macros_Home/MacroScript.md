@metadata title=Script Macro
@metadata tagstring=script js javascript macro alkira


#Script Macro

The script macro allows you to include javascripts in your text. There are two ways to include javascripts:

* as argument of the script macro, the argument refers to a javascript file
* as body of the script macro, the body is the javascript code itself


##Parameters

* src: the path to the javascript file

Instead of referring to a javascript file, you can add the javascript code to the markdown file. See the example below.


##Example

To call the script macro:

    [[script]]
    $('#mybutton').click(function() {
      alert("This is Incubaid!");
    });
    [[/script]]

    <button id="mybutton">Alert</button>
    
or

    [[script:src=http://path.to/javascriptfile.js/]]    

    
    
##Sample

[[script]]
$('#mybutton').click(function() {
  alert("This is Incubaid!");
});
[[/script]]

<button id="mybutton">Alert</button>