# Trac totalfield plugin

This Trac Plugin adds a Macro to compute the sum of a custom field values on a query.

Usage :

    [[TotalField(field_name, query)]]
    
Calculates the sum of a field_name values for the queried tickets.

The macro accepts a field_name and a comma-separated list of query parameters for the ticket selection,
in the form `key=value` as specified in TracQuery QueryLanguage.

Example:
   
        [[TotalField(field_name, milestone=Sprint 1)]]
   

Installation:

It can be installed as a "one file" plugin by copying the `total_filed.py` file in the plugin directory of your trac installation. 
