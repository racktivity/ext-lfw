<style>
.ui-state-highlight { height: 1.5em; line-height: 1.2em; }
</style>
<script language='javascript'>
$(document).ready(function(){
    
    $("#confirmdelete").dialog({autoOpen: false,
                                width: 550,
                                modal: true});
    
    $("#spaceform").dialog({autoOpen: false,
            width: 550,
            modal: true});
            
    $("#alert").dialog({
        autoOpen: false,
        width: 400,
        modal: true,
        buttons: {"Ok": function(){
                $(this).dialog("close");
            }}});
    
    var messagealert = function(title, message){
        $dialog = $("#alert");
        $dialog.dialog("option", "title", title);
        $dialog.find("#alertmessage").html(message);
        $dialog.dialog("open");
    };
    
    var confirmdelete = function(options){
        var options = $.extend({space: 'this',
                                ok: $.noop,
                                cancel: $.noop}, options);
        $("#confirmdelete > #space").text(options.space);
        $("#confirmdelete").dialog("option", "buttons", {'Ok': function(){
                                                                options.ok();
                                                                $(this).dialog("close");
                                                                },
                                                         'Cancel': function() {
                                                             options.cancel();
                                                             $(this).dialog("close");
                                                             }
                                                         });
        $("#confirmdelete").dialog("open");
    };
    
    
    
    var remotecall = function(options) {
        var options = $.extend({success: $.noop,
                                error: $.alerterror,
                                data: {}}, options);
                                    
        
        $.ajax({url: options.uri,
                dataType: 'json',
                data: options.data,
                success: options.success,
                error: options.error});
    };
    
    var listspaces = function(options) {
        var options = $.extend(options, {uri: LFW_CONFIG['uris']['listSpaces']});
        remotecall(options);
    };
    
    var deletespace = function(spacename, options){
        var options = $.extend(options, {uri: LFW_CONFIG['uris']['deleteSpace'],
                                        data: {name: spacename}});
        remotecall(options);
    };
    
    var createspace = function(spacename, options){
        var options = $.extend(options, {uri: LFW_CONFIG['uris']['createSpace'],
                                        data: {name: spacename}});
        remotecall(options);
    };
    
    var sortspaces = function(spaces, options){
        var options = $.extend(options, {uri: LFW_CONFIG['uris']['sortSpaces'],
                                        data: {"spaces": JSON.stringify(spaces)}});
        remotecall(options);
    };
    
    var editspace = function(name, newname, options){
        var options = $.extend(options, {uri: LFW_CONFIG['uris']['updateSpace'],
                                        data: {name: name,
                                               newname: newname}});
        remotecall(options);
    };
    
    var importspace = function(space, path, options){
        var options = $.extend(options, {uri: LFW_CONFIG['uris']['importSpace'],
                                        data: {space: space,
                                               filename: path}});
        remotecall(options);
    };
    
    var exportspace = function(space, path, options){
        var options = $.extend(options, {uri: LFW_CONFIG['uris']['exportSpace'],
                                        data: {space: space,
                                               filename: path}});
        remotecall(options);
    };
    
    console.log("Doing a list spaces call");
    
    var render = function(){
        listspaces({success: function(data){
                                var tbody = $("#spaceslist > tbody");
                                console.log("listspaces succeeded, rendering list...");
                                tbody.empty();
                                $.each(data, function(i, space){
                                    var renameText;
                                    var deleteText;
                                    var tdSpaceNameContent;
                                    var spaceElem;
                                    if ((space == "Admin") || (space == "IDE")) {
                                        renameText = "-";
                                        deleteText = "-";
                                        spaceElem = $("<span>").text(space);
                                    } else {
                                        renameText = "rename";
                                        deleteText = "delete";
                                        spaceElem = $("<a>", {href: "#/Admin/s_" + space}).text(space);
                                        
                                    }
                                    
                                    tbody.append($('<tr class="ui-state-default">').append('<td><span class="ui-icon ui-icon-arrowthick-2-n-s"></span></td>')
                                                          .append($("<td class='td_spacename'>").append(spaceElem))
                                                          .append($("<td>", {style: 'text-align: center'}).append($('<a>', {style: 'cursor: pointer'}).data('space', space).text(renameText).click(function() {
                                                                var space = $(this).data('space');
                                                                if ((space == 'IDE') || (space == 'Admin')){
                                                                    return;
                                                                }
                                                                $("#spaceform input").removeClass("ui-state-error").val(space);
                                                                var $dialog = $("#spaceform").dialog("option", "title", "Edit Space");
                                                                $("#spaceform").dialog("option", "buttons", {"Rename Space": function(){
                                                                                                            $input = $dialog.find("input").removeClass("ui-state-error");
                                                                                                            
                                                                                                            var spacename = $.trim($dialog.find("#name").val());
                                                                                                            if (spacename == ""){
                                                                                                                $input.addClass("ui-state-error");
                                                                                                                return;
                                                                                                            }
                                                                                                            if (space == spacename){
                                                                                                                $dialog.dialog("close");
                                                                                                                return;
                                                                                                            }
                                                                                                            
                                                                                                            editspace(space, spacename, {success: function(){
                                                                                                                $.fillSpacesList({success: function(){
                                                                                                                    $("#space").val("Admin");
                                                                                                                }});

                                                                                                                render();
                                                                                                                $dialog.dialog("close");
                                                                                                            }, error: $.alerterror});
                                                                                                        },
                                                                                                        
                                                                                                      "Cancel": function(){
                                                                                                          $(this).dialog("close");
                                                                                                        }});
                                                                $("#spaceform").keydown(function(e) {
                                                                    if (e.keyCode == 13) {
                                                                        var buttons = $( "#spaceform" ).dialog( "option", "buttons" );
                                                                        var button = buttons["Rename Space"];
                                                                        button();
                                                                    }
                                                                });
                                                                                
                                                                $("#spaceform").dialog("open");
                                                              })))
                                                          .append($("<td>", {style: 'text-align: center'}).append($('<a>', {style: 'cursor: pointer'}).data('space', space).text(deleteText).click(function(){
                                                                var space = $(this).data('space');
                                                                if ((space == 'IDE') || (space == 'Admin')){
                                                                     return;
                                                                }
                                                                confirmdelete({space: space,
                                                                         ok: function(){
                                                                             deletespace(space, {success: function(){
                                                                                    $.fillSpacesList({success: function(){
                                                                                        $("#space").val("Admin");
                                                                                    }});
                                                                                    render();
                                                                                 }});
                                                                         }});
                                                              }))));
                                });
                            }});
    };
    
    $("#createspace").button().click(function() {
        var $dialog = $("#spaceform").dialog("option", "title", "Create Space");
        $("#spaceform  input").removeClass("ui-state-error").val("");
        $("#spaceform").dialog("option", "buttons", {"Create Space": function(){
                                                    $input = $dialog.find("input").removeClass("ui-state-error");
                                                    
                                                    var spacename = $.trim($dialog.find("#name").val());
                                                    if (spacename == ""){
                                                        $input.addClass("ui-state-error");
                                                        return;
                                                    }
                                                    
                                                    createspace(spacename, {success: function(){
                                                        $.fillSpacesList({success: function(){
                                                            $("#space").val("Admin");
                                                        }});
                                                        render();
                                                        $dialog.dialog("close");
                                                    }, error: $.alerterror});
                                                },
                                                
                                              "Cancel": function(){
                                                  $(this).dialog("close");
                                                }});
                        
        $("#spaceform").dialog("open");
        $("#spaceform").keydown(function(e) {
            if (e.keyCode == 13) {
                var buttons = $( "#spaceform" ).dialog( "option", "buttons" );
                var button = buttons["Create Space"];
                button();
            }
        });
    });


    render();
    //Make spaces sortable
    var tablebody = $( "#spaceslist tbody")
    tablebody.sortable({
        placeholder: "ui-state-highlight",
        update: function(event, ui) {
            spaces = new Array()
            tds = $(".td_spacename")
            for (var i=0; i < tds.length; i++)
                spaces[i] = tds[i].textContent
            sortspaces(spaces, {success: function(){
                                                $.fillSpacesList({success: function(){
                                                    $("#space").val("Admin");
                                                }});
                                            },
                                error: $.alerterror});
        }
    });
    $( "#spaceslist tbody").disableSelection();
});

</script>

<div id='alert'>
<p id='alertmessage'></p>
</div>

<div id='confirmdelete' title='Delete Space'>
    Are you sure you want to delete <b id='space'></b> space?
    <div class='notice' style='margin-top: 25px;'>
    Deleting a space will delete all the pages in that space. There
    is noway to restore it back, so an "export" is adviced.
    </div>
</div>

<div id="spaceform" title="Create new space">
    <form>
    <fieldset>
        <label for="name">Name</label>
        <input type="text" name="name" id="name" class="text ui-widget-content ui-corner-all " />
    </fieldset>
    </form>
</div>

## Spaces

<table id='spaceslist' style='width: 80%;'>
<thead>
    <tr>
        <th></th>
        <th style='width: 50%;'>Space</th>
        <th style='text-align:center;'>Rename</th>
        <th style='text-align:center;'>Delete</th>
    </tr>
</thead>
<tbody>
</tbody>
</table>

<button id='createspace'>Create New Space</button>
