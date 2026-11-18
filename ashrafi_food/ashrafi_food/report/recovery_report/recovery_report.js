frappe.query_reports['Recovery Report'] = {
    filters: [
        
     	{
            fieldname: "pay_from",
            label: __("Pay From"),
            fieldtype: "Date",
	    default: frappe.datetime.add_days(frappe.datetime.nowdate(), -30)
			        },
          
          
       
        {
            fieldname: "pay_to",
            label: __("Pay To"),
            fieldtype: "Date",
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