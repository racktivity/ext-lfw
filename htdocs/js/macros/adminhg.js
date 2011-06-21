///TODO show error/ok sign?
///TODO seperate login from url
///TODO global integration into the admin space

var render = function(options) {
    var jq = $(this);

    options.addCss({id: "adminhg", tag: "style", params: "#adminhg-table td { vertical-align: middle; } " +
        "#adminhg-table td input.repository { width: 100%; } " +
        "#adminhg-table td span span.loading { width: 16px; height: 16px; left: 6px; position: absolute; }" +
        "#adminhg-table td span.loading-container { position: relative; }" +
        "#adminhg-table td.commands { width: 20%; }" });

    $.template("plugin.adminhg.table",
    "<table id='adminhg-table'><tr><th>Space</th><th>Repository</th><th>Command</th></tr>" +
        "{{each Spaces}}<tr id='${guid}'><td class='name'>${name}</td>" +
        "<td><input class='repository' type='text' value='${repository}' /></td>" +
        "<td class='commands'><button class='pull'>pull</button>&nbsp;<button class='push'>push</button>" +
        "<span class='loading-container'><span class='loading'>&nbsp;</span></span></td></tr>{{/each}}" +
    "</table>");

    //perform the pull
    function pull(spaceInfo, callback) {
        $(this).parents("tr").find("td span.loading").html("<img src='img/ajax-loader.gif' />");
        $.get(LFW_CONFIG.uris.hgPullSpace, spaceInfo, "json")
            .success($.proxy((callback ? callback : pullSuccess), this)).error($.proxy(pullError, this));
    }

    //perform the push
    function push(spaceInfo) {
        $(this).parents("tr").find("td span.loading").html("<img src='img/ajax-loader.gif' />");
        $.get(LFW_CONFIG.uris.hgPushSpace, spaceInfo, "json")
            .success($.proxy(pushSuccess, this)).error($.proxy(pushError, this));
    }

    //Our push was successful
    function pushSuccess(data) {
        $(this).parents("tr").find("td span.loading").empty();
        if (typeof(data) === "boolean") {
            if (!data) {
                if (confirm("Your local data is currently out of sync.\nIt is advisable to do a pull first.\n" +
                    "There might be some merge conflicts that you will need to solve later on.\n" +
                    "Perform a pull now?\n")) {

                        var spaceGuid = $(this).parents("tr")[0].id,
                            repository = $(this).parents("tr").find(".repository").val();
                            spaceInfo = {spaceGuid: spaceGuid, repository: repository, repo_username: "", repo_password: ""};
                        pull.apply(this, [spaceInfo, function() { push(spaceGuid, repository); }]);
                }
            } else {
                alert("Push done for space '" + $(this).parents("tr").find(".name").html() + "'.");
            }
        } else {
            pushError.call(this, data);
        }
    }

    //We had an error while pushing
    function pushError(data) {
        $(this).parents("tr").find("td span.loading").empty();
        if (typeof(data) === "object") {
            data = JSON.parse(data.responseText).exception;
        }
        alert("Error during push of space '" + $(this).parents("tr").find(".name").html() + "':\n" + data);
    }

    //Our pull was successful
    function pullSuccess(data) {
        $(this).parents("tr").find("td span.loading").empty();
        if (typeof(data) === "boolean" && data) {
            alert("Pull done for space '" + $(this).parents("tr").find(".name").html() + "'.");
        } else {
            pullError.call(this, data);
        }
    }

    //We had an error while pulling
    function pullError(data) {
        $(this).parents("tr").find("td span.loading").empty();
        if (typeof(data) === "object") {
            data = JSON.parse(data.responseText).exception;
        }
        alert("Error during pull of space '" + $(this).parents("tr").find(".name").html() + "':\n" + data);
    }

    //get the spaces
    $.get(LFW_CONFIG.uris.listSpaces, { fullInfo: true }, function(spaces) {
        jq.empty();
        jq.append($.tmpl("plugin.adminhg.table", { Spaces: spaces }));

        //make the push work
        jq.find("table td button.push").click(function() {
            var spaceGuid = $(this).parents("tr")[0].id,
                repository = $(this).parents("tr").find(".repository").val();
            push.call(this, {spaceGuid: spaceGuid, repository: repository, repo_username: "", repo_password: ""});
        });

        //make the pull work
        jq.find("table td button.pull").click(function() {
            var spaceGuid = $(this).parents("tr")[0].id,
                repository = $(this).parents("tr").find(".repository").val();
            pull.call(this, {spaceGuid: spaceGuid, repository: repository, repo_username: "", repo_password: ""});
        });
    });
};
register(render);
