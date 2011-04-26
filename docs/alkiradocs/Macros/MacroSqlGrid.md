#SQL Grid Macro
This macro executes a given SQL query and shows the result in a SQL grid, with support of paging.


## Parameters
* __dbconnection:__ name of the database connection, as configured on the database server
* __table:__ table name to select from
* __schema:__ schema name of the table, if any
* __sqlselect:__ your SQL select statement
* __link:__ name of the field in the query which links to $space\_$pagename or $space\_$type\_$pagename. The name to the link is the name of field.
* __sort:__ name of field on which you can sort
* __pagesize:__ maximum rows per page
* __width:__ width of the grid, by default 600
* __height:__ height of the grid, by default 400
* __fieldwidth:__ a dictionary which specifies the width of each field. If this is not provided, each field width is 80


##Remote database Configuration

To configure remote databases this configuration should be in file under location /opt/qbase5/cfg/qconfig/dbconnections.cfg

### Example configuration

    [db_sampleapp]
    dbtype = postgresql
    dbpasswd = 
    dblogin = sampleapp
    dbname = sampleapp
    dbserver = 127.0.0.1

##Macro Example

    <div class="macro macro_sqlgrid">
    {
        "dbconnection": "sampleapp",
        "table": "ui_view_page_list",
        "schema": "ui_page",
        "sqlselect": "SELECT ui_view_page_list.category, ui_view_page_list.name, ui_view_page_list.parent FROM ui_page.ui_view_page_list WHERE ui_view_page_list.space='Macros'",
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
    
    </div>
###### OR you can specify the columns you want to retrieve, Schema name, Table/View name and a dictionary of filter you want to use
    <div class="macro macro_sqlgrid">
    {
        "dbconnection": "sampleapp",
        "table": "ui_view_page_list",
        "schema": "ui_page",
        "columns": {
            "category": null,
            "name": "Macro name",
            "parent": "Parent guid"
            },
        "wheredict": {
            "space": "Macros"
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
    </div>



##Sample

<div class="macro macro_sqlgrid">
    {
        "dbconnection": "sampleapp",
        "table": "ui_view_page_list",
        "schema": "ui_page",
        "columns": {
            "category": null,
            "name": "Macro name",
            "parent": "Parent guid"
            },
        "wheredict": {
            "space": "Macros"
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

</div>

