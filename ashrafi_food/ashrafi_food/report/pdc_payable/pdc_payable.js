// Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["PDC Payable"] = {
	"filters": [
	 {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
			reqd:1,
            default: frappe.datetime.add_days(frappe.datetime.nowdate(), -20)
        },
          
          
       
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
			reqd:1,
            default: frappe.datetime.nowdate()
        },


	]
};
