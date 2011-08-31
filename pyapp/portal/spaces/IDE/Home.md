



<link rel=StyleSheet href="/static/lfw/js/libs/jstree/themes/classic/style.css" type="text/css" />
<script language="javascript" src="/static/lfw/js/libs/jstree/jquery.hotkeys.js"/>
<script language="javascript" src="/static/lfw/js/libs/jstree/jquery.jstree.js"/>

<div id="editortabs_container">
    <div id="editortabs">
        <ul>
        </ul>
    </div>
</div>

<script language='javascript'>
$(document).ready(function(){
    $("#editortabs").tabs({tabTemplate: "<li><a href='#{href}'>#{label}</a> <span title='Save' style='cursor: pointer; display: inline-block' class='ui-icon ui-icon-note'>Save</span> <span title='Close' style='cursor: pointer; display: inline-block' class='ui-icon ui-icon-close'>Close</span></li>",
                           panelTemplate: "<div>" +
                                            "<div id='fileid' class='ide-fileid'></div>" +
                                            "<div id='editorspace' style='height: 600px'></div>" +
                                          "</div>"});

    $(document).lock("ide.ready");
});
var setFontSizeSmall = function() {
    $("#editorspace").addClass("small");
};
var setFontSizeNormal = function() {
    $("#editorspace").removeClass("small");
};

</script>

[[widget:title=IDE]]
##Integrated Development Environment

Here you can edit your projects, first you need to create a project from the *Projects* page in the *Admin* space.

- Double click file to open it in the editor space.
- Right Click a file, or a directory for more options.

To work fullscreen, Click the expand-button on the top-right of the tab bar

<div class="small">
    <form>
        <span>Font size:</span>
        <input type="radio" name="fontsize" value="small" onClick="setFontSizeSmall();" checked /> Small
        <input type="radio" name="fontsize" value="normal" onClick="setFontSizeNormal();" /> Normal
    </form>
</div>

[[/widget]]
