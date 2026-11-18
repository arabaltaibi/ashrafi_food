// Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.query_reports['Payment Posting Date'] = {
    filters: [
        
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
			reqd:1,
            default: frappe.datetime.add_days(frappe.datetime.nowdate(), 0)
        },
          
          
       
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
			reqd:1,
            default: frappe.datetime.nowdate()
        },
	
        
      //  { fieldname: "territory", 
      //  label: __("Area"),
      //  fieldtype: "Link",
      //  options: "Territory"
       
	//     },
   

         {
            fieldname: "sales_person",
            label: __("Sales Men"),
            fieldtype: "Link",
            options: "User",
           
        },
         {
            fieldname: "mode_of_payment",
            label: __("Area"),
            fieldtype: "Link",
            options: "Mode of Payment",
           
        }

      
    ]
}