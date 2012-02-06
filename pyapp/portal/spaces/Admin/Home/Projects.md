##IDE Projects

[[widget:title=Help]]
###To Create a new project:

- You can create a new project by right clicking any part of the tree and then press *Create Project Here*
- Enter the *unique* project name, and press Ok
[[/widget]]

<div id="idetree" style='margin-top: 10px; margin-bottom: 10px; border: 1px solid lightgray'>
</div>


###Available Projects

<table id='projects'>
    <thead>
        <tr>
            <th>Project</th>
            <th>Path</th>
            <th>Delete</th>
        </tr>
    </thead>
    <tbody>
    </tbody>
</table>

<link rel="stylesheet" href="js/libs/jstree/themes/classic/style.css" type="text/css" />
<script language="javascript" src="js/libs/jstree/jquery.hotkeys.js"/>
<script language="javascript" src="js/libs/jstree/jquery.jstree.js"/>

<script>
$(document).ready(function() {
    var METHODS = {createproject: "createProject",
                   deleteproject: "deleteProject",
                   getprojects: "getProjects"};
               
    var remotecall = function(method, options) {
        var options = $.extend({success: $.noop,
                                error: $.alerterror,
                                data: {}}, options);
                                
        $.ajax({url: 'appserver/rest/ui/ide/' + method,
                type: 'POST',
                dataType: 'json',
                data: options.data,
                success: options.success,
                error: options.error});
    };
    
    var createProject = function(item) {
        var id = item.attr("id");
        var tree = this;
        $.prompt("Project Name?", {title: "Create Project Name",
                                   pattern: /.+/,
                                   error: "Project name can't be empty",
                                   value: tree.get_text(item),
                                   ok: function(name) {
                                       remotecall(METHODS.createproject, {data:{name: name,
                                                                                path: id},
                                                                          success: function(){
                                                                              listprojects();
                                                                          }});
                                    }});
    };
    
    $("#idetree").jstree({ plugins: ['themes', 'json_data', 'types', 'ui', 'contextmenu', 'crrm'],
                        ui: {
                            select_limit: 1,
                        },
                        types: {
                            types: { project: {icon: {image: 'img/editor/project.png'}},
                                     file: {icon: {image: 'img/editor/file.png'}},
                                     default: {}}
                        },
                        contextmenu: {
                            items: [{label: "Create Project Here",
                                     action: createProject}],
                        },
                        json_data: {
                                ajax: { url: 'appserver/rest/ui/ide/getProjectNode',
                                        data: function(n) {
                                            return {id: n.attr ? n.attr("id") : "."};
                                        }},
                            progressive_render : true
                            },
                        themes: {theme : "classic"},
                    });
    
    var listprojects = function(){
        remotecall(METHODS.getprojects, {success: function(projects){
            var body = $("#projects > tbody").empty();
            $.each(projects, function(){
                var project = this;
                var row = $("#project-row").tmpl(project);
                $("#delete", row).click(function(e){
                    e.preventDefault();
                    $.confirm("Are you sure you want to delete project '" + project.name + "' ?",
                                {title: "Delete Project",
                                ok: function(){
                                    remotecall(METHODS.deleteproject, {data: {name: project.name},
                                                                       success: function() {
                                                                           row.remove();
                                                                        }});
                                }});
                });
                body.append(row);
            });
        }});
    };
    
    listprojects();
});

</script>
<script id="project-row" type="text/x-jquery-tmpl">
  <tr>
    <td>${name}</td>
    <td>${path}</td>
    <td><a id='delete' href='#'>delete</a></td>
  </tr>
</script>
