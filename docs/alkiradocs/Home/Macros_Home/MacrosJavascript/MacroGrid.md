@metadata title=Grid Macro
@metadata tagstring=macro alkira grid

# Grid Macro
The grid macro is a macro that builds a table in which you can sort on the columns. 


#Parameters
The Grid macro does not accept parameters

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
  "height": 75
}
[[/grid]]	