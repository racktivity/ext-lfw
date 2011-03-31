# SQL Grid Macro

This macro executes a given query and shows the result in a sql grid, supports paging

## Parameters

* __dbname:__ Name of the database
* __sql:__ The sql statement to query (any select statement)
* __link:__ Name of the field in query which links to $space_$pagename or $space_$type_$pagename, name to the link is name of field
* __sort:__ Name of field that can be sorted
* __pagesize:__ Maximum rows per page

## Remote database Configuration

To configure remote databases this configuration should be in file under location /opt/qbase3/cfg/qconfig/dbconnections.cfg

### Example configuration

	[db_$nameofDbConnection]
	dbtype=postgresql #only supported for now
	dbserver=192....
	dblogin=
	dbpasswd=
	dbname=

## Macro Example

	<div class="macro macro_sqlgrid">
		{
			"dbname": "local",
			"sql": "SELECT view_page_list.category, view_page_list.name, view_page_list.parent, view_page_list.space FROM page.view_page_list",
			"link": "name",
			"sort": "name",
			"pagesize": 10
		}
	
	</div>

## Sample

<div class="macro macro_sqlgrid">
	{
		"dbname": "local",
		"sql": "SELECT view_page_list.category, view_page_list.name, view_page_list.parent, view_page_list.space FROM page.view_page_list",
		"link": "name",
		"sort": "name",
		"pagesize": 10
	}

</div>



