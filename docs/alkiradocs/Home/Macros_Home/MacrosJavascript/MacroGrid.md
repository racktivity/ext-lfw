@metadata title=Grid Macro
@metadata tagstring=macro alkira grid

# Grid Macro
The grid macro is a macro that builds a table in which you can sort on the columns. 


#Parameters
The Grid macro does not accept parameters, all data is provided in the body of the macro.

##Example

    [[grid]]
    {
      "sort": "Aggregated data", 
      "name": "", 
	  "pagesize": 10, 
	  "hidetitlebar": true, 
	  "autowidth": true, 
	  "data": [
	    {
	      "Aggregated data": "Apparent Power", 
	      "Value": "0.00"
	    }, 
	    {
	      "Aggregated data": "Power", 
	      "Value": "0.00"
	    }, 
	    {
	      "Aggregated data": "Active Energy", 
	      "Value": "0.00"
	    }, 
	    {
	      "Aggregated data": "Apparent Energy", 
	      "Value": "0.00"
	    }, 
	    {
	      "Aggregated data": "Current", 
	      "Value": "0.00"
	    }, 
	    {
	      "Aggregated data": "Co 2", 
	      "Value": "0.00"
	    }, 
	    {
	      "Aggregated data": "Voltage", 
	      "Value": "0.00"
	    }, 
	    {
	      "Aggregated data": "Frequency", 
	      "Value": "0.00"
	    }, 
	    {
	      "Aggregated data": "Power Factor", 
	      "Value": "0.00"
	    }
	  ], 
	  "columns": [
	    "Aggregated data", 
	    "Value"
	  ], 
      "model": [
	    {"sortable": false
	     "align": "center"
	     "width": 200	    
	    },
	    {"sortable": true
	    }
	  ], 
	    "model": [
	    {"sortable": false
	    },
	    {"sortable": true
	    }
	  ],
	  "height": 75
	}
	[[/grid]]
	
	
##Sample

[[grid]]
{
  "sort": "Aggregated data", 
  "name": "", 
  "pagesize": 10, 
  "hidetitlebar": true, 
  "autowidth": true, 
  "data": [
    {
      "Aggregated data": "Apparent Power", 
      "Value": "0.00"
    }, 
    {
      "Aggregated data": "Power", 
      "Value": "0.00"
    }, 
    {
      "Aggregated data": "Active Energy", 
      "Value": "0.00"
    }, 
    {
      "Aggregated data": "Apparent Energy", 
      "Value": "0.00"
    }, 
    {
      "Aggregated data": "Current", 
      "Value": "0.00"
    }, 
    {
      "Aggregated data": "Co 2", 
      "Value": "0.00"
    }, 
    {
      "Aggregated data": "Voltage", 
      "Value": "0.00"
    }, 
    {
      "Aggregated data": "Frequency", 
      "Value": "0.00"
    }, 
    {
      "Aggregated data": "Power Factor", 
      "Value": "0.00"
    }
  ], 
  "columns": [
    "Aggregated data", 
    "Value"
  ],
  "model": [
	    {"sortable": false
	     "align": "center"
	     "width": 200	    
	    },
	    {"sortable": true
	    }
	  ], 
  "height": 75
}
[[/grid]]	

The model section is used for the layout of your table. This section is a list of dicts, where each dict represents one column. The first dict for the first column, and so on...

* sortable: true/false, if true, you can sort the column in ascending or descending order
* align: left (default), center, right; alignment of the values
* width: width of the column in pixels