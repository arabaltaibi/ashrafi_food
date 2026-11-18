// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Daily Sales Activity"] = {
	"filters": [
        {
			"fieldname":"sales_man",
			"label": __("SalesMan"),
			"fieldtype": "Link",
			"options": "User",
		},
		{
			"fieldname":"vehicle",
			"label": __("Vehicle No."),
			"fieldtype": "Link",
			"options": "Vehicle",
		},
		{
			"fieldname":"area",
			"label": __("Area"),
			"fieldtype": "Link",
			"options": "Territory",
		},
		{
			"fieldname":"supervisor",
			"label": __("Supervisor"),
			"fieldtype": "Link",
			"options": "Sales Person",
		},
		
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"width": "60px"
		},
	]
};
