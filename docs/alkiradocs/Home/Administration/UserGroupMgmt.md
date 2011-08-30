@metadata title=User and Group Management
@metadata order=10
@metadata tagstring=user group management

[PyApp]: #/PyLabsApps/Home 
[imgNewUser]: images/images50/md_images/newuser.png
[imgChangePwd]: images/images50/md_images/changepwd.png
[imgRemoveUser]: images/images50/md_images/removeuser.png
[imgUserDetail]: images/images50/md_images/userdetail.png
[imgSelectGroup]: images/images50/md_images/selectgroup.png
[imgNewGroup]: images/images50/md_images/newgroup.png
[imgRenameGroup]: images/images50/md_images/renamegroup.png
[imgAssignRule]: images/images50/md_images/assignrule.png
[imgRevokeRule]: images/images50/md_images/revokerule.png
[imgRemoveGroup]: images/images50/md_images/removegroup.png


#Alkira User and Group Management

The integrated user and group management, via Alkira, is used to manage the complete authentication and authorization of a PyLabs Application ([PyApp][]).
These functionalities are all available in the __Admin__ space of the PyApp.

This section covers the following topics...

[[toc/]]


##User Management
In the __Users__ section of the Admin space, you can:

* add new users
* change user passwords
* remove users 
* add users to different groups


###Adding a New User
To add new users to a PyApp:

1. Select the __Admin__ space of the PyApp.
2. Go to the __Users__ page. An overview of existing users and groups appears.
3. Click __Add User__, a form appears to fill out the user credentials.
<br/>
<br/>
![newUser][imgNewUser]
<br/>
<br/>
4. Fill out the user data and click __Add__.
The user appears in the list.


###Changing User Passwords
To change the password of a user:

1. Select the __Admin__ space of the PyApp.
2. Go to the __Users__ page. An overview of existing users and groups appears.
3. Click __Change Password__ next to the concerned user. A form appears to change the password.
<br/>
<br/>
![ChangePwd][imgChangePwd]
<br/>
<br/>
4. Enter a new password and click __Change__.
The password is updated. 

The new password must be applied upon the next login of the user.


###Removing a User
To remove a user:

1. Select the __Admin__ space of the PyApp.
2. Go to the __Users__ page. An overview of existing users and groups appears.
3. Click __Remove__ next to the user that your want to remove. A confirmation window appears.
<br/>
<br/>
![RemoveUser][imgRemoveUser]
<br/>
<br/>
4. Click __Remove__ to confirm the removal of the user. The user permissions are immediately revoked.
If the user has an open session, he is no longer able to perform new actions.


###Adding a User to Groups
To add a user to a group:

1. Select the __Admin__ space of the PyApp.
2. Go to the __Users__ page. An overview of existing users and groups appears.
3. Click the name of a user. The list of groups, to which the user belongs, appears
<br/>
<br/>
![UserDetail][imgUserDetail]
<br/>
<br/>
4. Click __Add to group__. A form appears with the list of available groups.
<br/>
<br/>
![SelectGroup][imgSelectGroup]
<br/>
<br/>
5. Select to group to which you want to add the user and click __Add__.
The selected group appears in the list of groups.

The user must restart his session to apply the changes.


##Group Management
In the __Users__ section of the Admin space, you can also manage the user groups. By default there are five groups defined, each with their own set of rules.
Update the groups to your own needs.

In this section you learn to:

* create new groups
* rename groups
* assign rules for a group
* revoke rules in a group
* remove groups


###Creating a Group
To create a new group:

1. Select the __Admin__ space of the PyApp.
2. Go to the __Users__ page. An overview of existing users and groups appears.
3. Click __Add Group__, a form appears to fill out the group credentials.
<br/>
<br/>
![newGroup][imgNewGroup]
<br/>
<br/>
4. Provide a group name and click __Add__.
The group appears in the list.


###Renaming a Group
To rename a group:

1. Select the __Admin__ space of the PyApp.
2. Go to the __Users__ page. An overview of existing users and groups appears.
3. Click the name of a group. The details of the group are expanded.
4. Click __Rename__ to rename the group. A form appears to rename the group.
<br/>
<br/>
![RenameGroup][imgRenameGroup]
<br/>
<br/>
5. Update the group name and click __Rename__.
The group name is updated.


###Assigning Rules for a Group
To create a rule for a group:

1. Select the __Admin__ space of the PyApp.
2. Go to the __Users__ page. An overview of existing users and groups appears.
3. Click the name of a group for which you want to create a rule. The details of the group are expanded.
4. Click __Assign rule__, a form appears with a list of rules.
<br/>
<br/>
![AssighRule][imgAssignRule]
<br/>
<br/>
5. Select the proper rule and click __Add__.
Repeat this to assign more rules to the group.


###Revoking a Rule in a Group
To revoke a rule in a group:

1. Select the __Admin__ space of the PyApp.
2. Go to the __Users__ page. An overview of existing users and groups appears.
3. Click the name of a group for which you want to revoke a rule. The details of the group are expanded.
4. Click __Revoke__ next to the rule that you want to revoke. A confirmation window appears.
<br/>
<br/>
![RevokeRule][imgRevokeRule]
<br/>
<br/>
5. Click __Revoke__ to confirm the removal of the rule from the group. The rule is immediately revoked and disappears from the list of rules.


###Removing a Group
To remove a group:

1. Select the __Admin__ space of the PyApp.
2. Go to the __Users__ page. An overview of existing users and groups appears.
3. Click __Remove__ next to the group that your want to remove. A confirmation window appears.
<br/>
<br/>
![RemoveGroup][imgRemoveGroup]
<br/>
<br/>
4. Click __Remove__ to confirm the removal of the group. 
The group is immediately removed from the PyApp.
