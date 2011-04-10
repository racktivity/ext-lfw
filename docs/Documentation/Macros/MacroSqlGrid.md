# SQL Grid Macro

This macro executes a given query and shows the result in a sql grid, supports paging

## Parameters

* __dbconnection:__ Name of the database connection (connection with this name must be configured on the server)
* __table:__ Table name to select from
* __schema:__ Name of schema this table exists
* __sqlselect:__ Any select statement
* __link:__ Name of the field in query which links to $space_$pagename or $space_$type_$pagename, name to the link is name of field
* __sort:__ Name of field that can be sorted
* __pagesize:__ Maximum rows per page
* __width:__ Width of the grid, if not given default is 600
* __height:__ Height of the grid, if not given default is 400
* __fieldwidth:__ Dict specifies width of each field specified if not given default width of each field is 80

## Remote database Configuration

To configure remote databases this configuration should be in file under location /opt/qbase3/cfg/qconfig/dbconnections.cfg

### Example configuration

	[db_$nameofDbConnection]
	dbtype=postgresql #only supported for now
	dbserver=127.0.0.1
	dblogin=qbase
	dbpasswd=rooter
	dbname=portal

## Macro Example

	<div class="macro macro_sqlgrid">
	{
		"dbconnection": "local",
		"table": "view_page_list",
		"schema": "page",
		"sqlselect": "SELECT view_page_list.category, view_page_list.name, view_page_list.parent FROM page.view_page_list WHERE view_page_list.space='Documentation'",
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

## Sample

<div class="macro macro_sqlgrid">
	{
		"dbconnection": "local",
		"table": "view_page_list",
		"schema": "page",
		"sqlselect": "SELECT view_page_list.category, view_page_list.name, view_page_list.parent FROM page.view_page_list WHERE view_page_list.space='Documentation'",
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



