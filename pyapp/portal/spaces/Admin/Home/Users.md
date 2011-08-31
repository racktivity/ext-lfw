
<script language="javascript">
$(document).ready(function() {
    var getRuleName = function(rule, toText) {
        var contextName = "ALL";
        if (rule.context.hasOwnProperty("space")) {
            contextName = rule.context.space;
        }
        return rule["function"] + (toText ? " ON " : " <b>ON</b> ") + contextName;
    };

    var UserPanel = function(user) {
        var body = $("#user-panel").tmpl(user),
            that = this;

        //add groups
        this.refreshGroups = function() {
            var userGroups = $(".user-groups", body);
            userGroups.empty();
            var i;
            for (i = 0; i < user.groups.length; ++i) {
                var groupguid = user.groups[i];
                if (groupsInfo.hasOwnProperty(groupguid)) {
                    var group = groupsInfo[groupguid];
                    userGroups.append("<tr><td>" + group.name + "</td>" +
                        "<td><a href='' id='" + user.guid + group.guid + "' class='user-remove-from-group'>Remove</a></td></tr>");
                }
            }

            $(".user-remove-from-group", body).click(function(e) {
                e.preventDefault();
                var groupguid = $(this).attr("id").replace(user.guid, ""),
                    userAndGroup = $.extend({}, user, { group: groupsInfo[groupguid].name });
                    removeDialog = $("#user-remove-from-group-dialog").tmpl(userAndGroup);
                $(document).append(removeDialog);
                removeDialog.dialog({
                    resizable: false,
                    modal: true,
                    height: "auto",
                    width: "auto",
                    buttons: {
                        "Remove": function() {
                            $.get(LFW_CONFIG.uris.removeUserFromGroup, { userguid: user.guid, groupguid: groupguid },
                                function() {
                                    var i;
                                    for (i = 0; i < user.groups.length; ++i) {
                                        if (user.groups[i] === groupguid) {
                                            user.groups.splice(i, 1);
                                            break;
                                        }
                                    }
                                    that.refreshGroups();
                                });
                            $(this).dialog("close");
                            removeDialog.remove();
                        },
                        "Cancel": function() {
                            $(this).dialog("close");
                            removeDialog.remove();
                        }
                    }
                });
            });
        };

        $("button", body).button();

        $(".user-edit", body).click(function(e) {
            e.preventDefault();
            $(this).parents("tr").nextAll(".user-edit-panel:first").toggle();
        });

        $(".user-changepass", body).click(function(e) {
            e.preventDefault();
            var changepassDialog = $("#user-changepass-dialog").tmpl(user);
            $(document).append(changepassDialog);
            changepassDialog.dialog({
                resizable: false,
                modal: true,
                height: "auto",
                width: "auto",
                buttons: {
                    "Change": function() {
                        var password = $(".user-pass", changepassDialog).val();
                        $.post(LFW_CONFIG.uris.updateUser, { userguid: user.guid, password: password });
                        $(this).dialog("close");
                        changepassDialog.remove();
                    },
                    "Cancel": function() {
                        $(this).dialog("close");
                        changepassDialog.remove();
                    }
                }
            });
        });

        $(".user-remove", body).click(function(e) {
            e.preventDefault();
            var removeDialog = $("#user-remove-dialog").tmpl(user);
            $(document).append(removeDialog);
            removeDialog.dialog({
                resizable: false,
                modal: true,
                height: "auto",
                width: "auto",
                buttons: {
                    "Remove": function() {
                        $.get(LFW_CONFIG.uris.deleteUser, { userguid: user.guid }, function() {
                            var i;
                            for (i = 0; i < users.length; ++i) {
                                if (users[i] === user) {
                                    users.splice(i, 1);
                                    break;
                                }
                            }
                            updateUsers();
                        });
                        $(this).dialog("close");
                        removeDialog.remove();
                    },
                    "Cancel": function() {
                        $(this).dialog("close");
                        removeDialog.remove();
                    }
                }
            });
        });

        $(".user-rename", body).click(function(e) {
            var renameDialog = $("#user-rename-dialog").tmpl(user);
            $(document).append(renameDialog);
            renameDialog.dialog({
                resizable: false,
                modal: true,
                height: "auto",
                width: "auto",
                buttons: {
                    "Rename": function() {
                        var newName = $(".user-name", renameDialog).val();
                        $.post(LFW_CONFIG.uris.updateUser, { userguid: user.guid, name: newName }, function() {
                            user.name = newName;
                            updateUsers();
                        });
                        $(this).dialog("close");
                        renameDialog.remove();
                    },
                    "Cancel": function() {
                        $(this).dialog("close");
                        renameDialog.remove();
                    }
                }
            });
        });

        $(".user-add-to-group", body).click(function(e) {
            var userAndGroups = $.extend({}, user, { groups: groups }),
                addgroupDialog = $("#user-add-to-group-dialog").tmpl(userAndGroups);
            $(document).append(addgroupDialog);
            addgroupDialog.dialog({
                resizable: false,
                modal: true,
                height: "auto",
                width: "auto",
                buttons: {
                    "Add": function() {
                        var groupguid = $(".user-group", addgroupDialog).val();
                        $.post(LFW_CONFIG.uris.addUserToGroup,
                            { userguid: user.guid, groupguid: groupguid },
                            function() {
                                user.groups.push(groupguid);
                                that.refreshGroups();
                            });
                        $(this).dialog("close");
                        addgroupDialog.remove();
                    },
                    "Cancel": function() {
                        $(this).dialog("close");
                        addgroupDialog.remove();
                    }
                }
            });
        });

        this.getDom = function() {
            return body;
        };

        this.refreshGroups();
    };

    var GroupItem = function(group) {
        var body = $("#group-panel").tmpl(group),
            that = this;

        $("button", body).button();

        //add rules
        this.refreshRules = function() {
            var groupRules = $(".group-rules", body);
            groupRules.empty();
            var i;
            if (!group.hasOwnProperty("rules")) {
                return;
            }
            for (i = 0; i < group.rules.length; ++i) {
                var rule = group.rules[i];
                groupRules.append("<tr><td>" + getRuleName(rule) + "</td>" +
                    "<td><a href='' id='" + group.guid + rule.guid + "' class='group-remove-rule'>Revoke</a></td></tr>");
            }

            $(".group-remove-rule", body).click(function(e) {
                e.preventDefault();
                var ruleguid = $(this).attr("id").replace(group.guid, ""),
                    rulename = $(this).parents("tr:first").find("td:first").text(),
                    groupAndRule = { "group": group.name, "rule": rulename },
                    removeDialog = $("#group-remove-rule-dialog").tmpl(groupAndRule);

                var i,
                    rule;
                for (i = 0; i < group.rules.length; ++i) {
                    if (group.rules[i].guid === ruleguid) {
                        rule = group.rules[i];
                        break;
                    }
                }

                $(document).append(removeDialog);
                removeDialog.dialog({
                    resizable: false,
                    modal: true,
                    height: "auto",
                    width: "auto",
                    buttons: {
                        "Revoke": function() {
                            $.get(LFW_CONFIG.uris.revokeRule, { groupguids: group.guid,
                                "function": rule["function"], context: $.toJSON(rule.context) },
                                function() {
                                    var i;
                                    for (i = 0; i < group.rules.length; ++i) {
                                        if (group.rules[i] === rule) {
                                            group.rules.splice(i, 1);
                                            break;
                                        }
                                    }
                                    that.refreshRules();
                                });
                            $(this).dialog("close");
                            removeDialog.remove();
                        },
                        "Cancel": function() {
                            $(this).dialog("close");
                            removeDialog.remove();
                        }
                    }
                });
            });
        };

        $(".group-edit", body).click(function(e) {
            e.preventDefault();
            $(this).parents("tr").nextAll(".group-edit-panel:first").toggle();
        });

        $(".group-remove", body).click(function(e) {
            e.preventDefault();
            var removeDialog = $("#group-remove-dialog").tmpl(group);
            $(document).append(removeDialog);
            removeDialog.dialog({
                resizable: false,
                modal: true,
                height: "auto",
                width: "auto",
                buttons: {
                    "Remove": function() {
                        $.get(LFW_CONFIG.uris.deleteGroup, { groupguid: group.guid }, function() {
                            var i;
                            for (i = 0; i < groups.length; ++i) {
                                if (groups[i] === group) {
                                    groups.splice(i, 1);
                                    break;
                                }
                            }
                            delete groupsInfo[group.guid];
                            updateUsers();
                            updateGroups();
                        });
                        $(this).dialog("close");
                        removeDialog.remove();
                    },
                    "Cancel": function() {
                        $(this).dialog("close");
                        removeDialog.remove();
                    }
                }
            });
        });

        $(".group-rename", body).click(function(e) {
            var renameDialog = $("#group-rename-dialog").tmpl(group);
            $(document).append(renameDialog);
            renameDialog.dialog({
                resizable: false,
                modal: true,
                height: "auto",
                width: "auto",
                buttons: {
                    "Rename": function() {
                        var newName = $(".group-name", renameDialog).val();
                        $.post(LFW_CONFIG.uris.updateGroup, { groupguid: group.guid, name: newName }, function() {
                            group.name = newName;
                            updateGroups();
                        });
                        $(this).dialog("close");
                        renameDialog.remove();
                    },
                    "Cancel": function() {
                        $(this).dialog("close");
                        renameDialog.remove();
                    }
                }
            });
        });

        $(".group-add-rule", body).click(function(e) {
            var groupAndRules = $.extend({}, group, { rules: possibleRules }),
                addruleDialog = $("#group-add-rule-dialog").tmpl(groupAndRules);
            $(document).append(addruleDialog);
            addruleDialog.dialog({
                resizable: false,
                modal: true,
                height: "auto",
                width: "auto",
                buttons: {
                    "Add": function() {
                        var rulenr = parseInt($(".group-rule", addruleDialog).val(), 10),
                            rule = possibleRules[rulenr];
                        $.post(LFW_CONFIG.uris.assignRule,
                            { groupguids: group.guid, "function": rule["function"], context: $.toJSON(rule.context) },
                            function() {
                                getRules(function() {
                                    updateRules();
                                    that.refreshRules();
                                });
                            });
                        $(this).dialog("close");
                        addruleDialog.remove();
                    },
                    "Cancel": function() {
                        $(this).dialog("close");
                        addruleDialog.remove();
                    }
                }
            });
        });


        this.getDom = function() {
            return body;
        };

        this.refreshRules();
    };

    // Apply ui to all buttons
    $("button", document).button();

    // Make add buttons work
    $("#user-add").click(function() {
        var addDialog = $("#user-add-dialog").tmpl();
        $(document).append(addDialog);
        addDialog.dialog({
            resizable: false,
            modal: true,
            height: "auto",
            width: "auto",
            buttons: {
                "Add": function() {
                    var login = $(".user-login", addDialog).val(),
                        password = $(".user-pass", addDialog).val(),
                        name = $(".user-name", addDialog).val();
                    $.post(LFW_CONFIG.uris.createUser, { login: login, password: password, name: name },
                        function() {
                            getUsers(updateUsers);
                        });
                    $(this).dialog("close");
                    addDialog.remove();
                },
                "Cancel": function() {
                    $(this).dialog("close");
                    addDialog.remove();
                }
            }
        });
    });

    $("#group-add").click(function() {
        var addDialog = $("#group-add-dialog").tmpl();
        $(document).append(addDialog);
        addDialog.dialog({
            resizable: false,
            modal: true,
            height: "auto",
            width: "auto",
            buttons: {
                "Add": function() {
                    var name = $(".group-name", addDialog).val();
                    $.post(LFW_CONFIG.uris.createGroup, { name: name },
                        function() {
                            getGroups(updateGroups);
                        });
                    $(this).dialog("close");
                    addDialog.remove();
                },
                "Cancel": function() {
                    $(this).dialog("close");
                    addDialog.remove();
                }
            }
        });
    });

    var groupsInfo = {},
        groups = [],
        users = [],
        rules = [],
        possibleRules = [];

    // users
    var getUsers = function(callback) {
        $.ajax({
            url: LFW_CONFIG.uris.users,
            dataType: "json",
            success: function(data) {
                users = data;
                callback.call(this);
            }
        });
    };

    var updateUsers = function() {
        var usersTable = $("#users");
        usersTable.empty();
        var i;
        for (i = 0; i < users.length; ++i) {
            usersTable.append(new UserPanel(users[i]).getDom());
        }
    };

    // groups
    var getGroups = function(callback) {
        $.ajax({
            url: LFW_CONFIG.uris.groups,
            dataType: "json",
            success: function(data) {
                groups = data;
                var i;
                for (i = 0; i < groups.length; ++i) {
                    var group = groups[i];
                    groupsInfo[group.guid] = group;
                }
                callback.call(this);
            }
        });
    };

    var updateGroups = function() {
        var groupsTable = $("#groups");
        groupsTable.empty();
        var i;
        for (i = 0; i < groups.length; ++i) {
            groupsTable.append(new GroupItem(groups[i]).getDom());
        }
    };

    // rules
    var getRules = function(callback) {
        $.ajax({
            url: LFW_CONFIG.uris.rules,
            dataType: "json",
            success: function(data) {
                rules = data;
                callback.call(this);
            }
        });
    };

    var updateRules = function() {
        var i,
            j;
        for (i = 0; i < groups.length; ++i) {
            delete groups[i].rules;
        }
        for (i = 0; i < rules.length; ++i) {
            var rule = rules[i];
            rule.context = $.parseJSON(rule.context);

            for (j = 0; j < rule.groups.length; ++j) {
                var group = groupsInfo[rule.groups[j]];
                if (!group.hasOwnProperty("rules")) {
                    group.rules = [];
                }
                group.rules.push(rule);
            }
        }
    };

    var getPossibleRules = function(callback) {
        $.ajax({
            url: LFW_CONFIG.uris.listPossibleRules,
            dataType: "json",
            success: function(data) {
                possibleRules = data;
                var i;
                for (i = 0; i < possibleRules.length; ++i) {
                    var rule = possibleRules[i];
                    rule.name = getRuleName(rule, true);
                }
                //sort rules
                possibleRules.sort(function(a, b) {
                    if (a.name < b.name) {
                        return -1;
                    } else if (a.name > b.name) {
                        return 1;
                    } else {
                        return 0;
                    }
                });
                callback.call(this);
            }
        });
    };

    var updateAll = function() {
        updateRules();
        updateUsers();
        updateGroups();
    };

    var todo = 4;
    var ajaxDone = function() {
        --todo;
        if (!todo) {
            updateAll();
        }
    };
    getGroups(ajaxDone);
    getUsers(ajaxDone);
    getRules(ajaxDone);
    getPossibleRules(ajaxDone);
});

</script>

## Users
<button id="user-add">Add User</button>

<table>
    <thead>
        <tr><th>Name</th><th>Change Password</th><th>Remove</th></tr>
    </thead>
    <tbody id='users'>
    </tbody>
</table>

<div id="users" />

## Groups
<button id="group-add">Add Group</button>

<table>
    <thead>
        <tr><th>Name</th><th>Remove</th></tr>
    </thead>
    <tbody id='groups'>
    </tbody>
</table>

<script id="user-panel" type="text/x-jquery-tmpl">
    <tr>
        <td><a href="" class="user-edit">${name}</a></td>
        <td><a href="" class="user-changepass">Change Password</a></td>
        <td><a href="" class="user-remove">Remove</a></td>
    </tr>
    //Added to get the color alternating right
    <tr style="display: none;"><td colspan="3" /></tr>

    <tr class="user-edit-panel" style="display: none">
        <td colspan="3" style="border-bottom: 1px solid;">
            <div style="margin-left: 10px;">
                <button class="user-rename">Rename</button>
                <table style='margin-top: 5px; margin-buttom: 5px;'>
                    <thead>
                        <tr>
                            <th>Group Name</th>
                            <th>Remove</th>
                        </tr>
                    </thead>
                    <tbody class='user-groups'>
                    </tbody>
                </table>
                <button class='user-add-to-group'>Add to group</button>
            </div>
        </td>
    </tr>
</script>

<script id="group-panel" type="text/x-jquery-tmpl">
    <tr>
        <td><a href="" class="group-edit">${name}</a></td>
        <td><a href="" class="group-remove">Remove</a></td>
    </tr>
    //Added to get the color alternating right
    <tr style="display: none;"><td colspan="3" /></tr>

    <tr class="group-edit-panel" style="display: none">
        <td colspan="2" style="border-bottom: 1px solid;">
            <div style="margin-left: 10px;">
                <button class="group-rename">Rename</button>
                <table style='margin-top: 5px; margin-buttom: 5px;'>
                    <thead>
                        <tr>
                            <th>Rule Name</th>
                            <th>Revoke</th>
                        </tr>
                    </thead>
                    <tbody class='group-rules'>
                    </tbody>
                </table>
                <button class='group-add-rule'>Assign rule</button>
            </div>
        </td>
    </tr>
</script>

<script id="user-remove-dialog" type="text/x-jquery-tmpl">
    <div title="Remove ${name}" style="display: none;">
        <span class="ui-icon ui-icon-alert" style="float: left; margin: 0 7px 20px 0;" />
        Are you sure you want to remove user "${name}"?
    </div>
</script>

<script id="user-rename-dialog" type="text/x-jquery-tmpl">
    <div title="Rename ${name}" style="display: none;">
        <table>
            <tr><td style="vertical-align: middle;">Name:</td><td><input type="text" style="width: 100%;" class="user-name" value="${name}" /></td></tr>
        </table>
    </div>
</script>

<script id="user-changepass-dialog" type="text/x-jquery-tmpl">
    <div title="Change password of ${name}" style="display: none;">
        <table>
            <tr><td style="vertical-align: middle;">Password:</td><td><input type="password" style="width: 100%;" class="user-pass" /></td></tr>
        </table>
    </div>
</script>

<script id="user-add-to-group-dialog" type="text/x-jquery-tmpl">
    <div title="Add user ${name} to a group" style="display: none;">
        <select class="user-group" style="width: 90%;">
            {{each(i, group) $data.groups}}
                <option value="${group.guid}">${group.name}</option>
            {{/each}}
        </select>
    </div>
</script>

<script id="user-remove-from-group-dialog" type="text/x-jquery-tmpl">
    <div title="Remove ${name} from "${group}" style="display: none;">
        <span class="ui-icon ui-icon-alert" style="float: left; margin: 0 7px 20px 0;" />
        Are you sure you want to remove user "${name}" from group "${group}"?
    </div>
</script>

<script id="user-add-dialog" type="text/x-jquery-tmpl">
    <div title="Add user" style="display: none;">
        <table>
            <tr><td style="vertical-align: middle;">Login:</td><td><input type="text" style="width: 100%;" class="user-login" /></td></tr>
            <tr><td style="vertical-align: middle;">Password:</td><td><input type="password" style="width: 100%;" class="user-pass" /></td></tr>
            <tr><td style="vertical-align: middle;">Name:</td><td><input type="text" style="width: 100%;" class="user-name" /></td></tr>
        </table>
    </div>
</script>

<script id="group-add-dialog" type="text/x-jquery-tmpl">
    <div title="Add group" style="display: none;">
        <table>
            <tr><td style="vertical-align: middle;">Name:</td><td><input type="text" style="width: 100%;" class="group-name" /></td></tr>
        </table>
    </div>
</script>

<script id="group-remove-dialog" type="text/x-jquery-tmpl">
    <div title="Remove ${name}" style="display: none;">
        <span class="ui-icon ui-icon-alert" style="float: left; margin: 0 7px 20px 0;" />
        Are you sure you want to remove group "${name}"?
    </div>
</script>

<script id="group-rename-dialog" type="text/x-jquery-tmpl">
    <div title="Rename ${name}" style="display: none;">
        <table>
            <tr><td style="vertical-align: middle;">Name:</td><td><input type="text" style="width: 100%;" class="group-name" value="${name}" /></td></tr>
        </table>
    </div>
</script>

<script id="group-remove-rule-dialog" type="text/x-jquery-tmpl">
    <div title="Revoke ${rule} from ${group}" style="display: none;">
        <span class="ui-icon ui-icon-alert" style="float: left; margin: 0 7px 20px 0;" />
        Are you sure you want to revoke rule "${rule}" from group "${group}"?
    </div>
</script>

<script id="group-add-rule-dialog" type="text/x-jquery-tmpl">
    <div title="Assign rule" style="display: none;">
        <table>
            <tr>
                <td style="vertical-align: middle;">
                    <select class="group-rule">
                        {{each(i, rule) $data.rules}}
                            <option value="${i}">${rule.name}</option>
                        {{/each}}
                    </select>
                </td>
            </tr>
        </table>
    </div>
</script>
