#SQL Grid Macro
The `sqlgrid` macro executes a given SQL query and shows the result in a SQL grid, with support of paging.


## Parameters
The `sqlgrid` macro does not accept parameters, the parameters are all defined in the body of the macro.

* __dbconnection:__ name of the database connection, as configured on the database server
* __name:__ name displayed at the top of the grid, default SQL Grid
* __table:__ table name to select from
* __schema:__ schema name of the table, if any
* __sqlselect:__ your SQL select statement, to be used without the `columns` and `wheredict` parameters
* __columns:__: columns of the table that you want to display, do not combine with the `sqlselect` parameter
* __wheredict:__: the filter of your data, do not combine with the `sqlselect` parameter
* __sort:__ name of field on which you can sort
* __pagesize:__ maximum rows per page
* __width:__ width of the grid, by default 600
* __height:__ height of the grid, by default 400
* __fieldwidth:__ a dictionary which specifies the width of each field. If this is not provided, each field width is 80


##Remote database Configuration

To configure remote databases this configuration should be in file under location `/opt/qbase5/cfg/qconfig/dbconnections.cfg`.

### Example configuration

    [db_sampleapp]
    dbtype = postgresql
    dbpasswd = 
    dblogin = sampleapp
    dbname = sampleapp
    dbserver = 127.0.0.1

##Macro Example
Using the `sqlselect` parameter:

    [[sqlgrid]]
    {
        "dbconnection": "sampleapp",
        "table": "ui_view_page_list",
        "schema": "ui_page",
        "sqlselect": "SELECT ui_view_page_list.category, ui_view_page_list.name, ui_view_page_list.parent FROM ui_page.ui_view_page_list WHERE ui_view_page_list.space='doc'",
        "link": "name",
        "sort": "name",
        "pagesize": 10,
        "width": 600,
        "height": 200,
        "fieldwidth": {
            "category": 40,
            "name": 80,
            "parent": 160
        }
    }
    [[/sqlgrid]]

Using the `columns` and `wheredict` parameters:

    [[sqlgrid]]
    {
        "dbconnection": "sampleapp",
        "table": "ui_view_page_list",
        "schema": "ui_page",
        "columns": {
            "category": null,
            "name": "Page name",
            "parent": "Parent guid"
            },
        "wheredict": {
            "space": "alkiradocs"
            },
        "link": "Macro name",
        "sort": "name",
        "pagesize": 10,
        "width": 600,
        "height": 200,
        "fieldwidth": {
            "category": 40,
            "name": 80,
            "parent": 160
        }
    }
    [[/sqlgrid]]



##Sample

[[sqlgrid]]
    {
        "dbconnection": "sampleapp",
        "table": "ui_view_page_list",
        "schema": "ui_page",
        "columns": {
            "category": null,
            "name": "Page name",
            "parent": "Parent guid"
            },
        "wheredict": {
            "space": "alkiradocs"
            },
        "link": "Macro name",
        "sort": "name",
        "pagesize": 10,
        "width": 600,
        "height": 200,
        "fieldwidth": {
            "category": 40,
            "name": 80,
            "parent": 160
        }
    }
[[/sqlgrid]]

