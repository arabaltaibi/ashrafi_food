// Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Warehouse Wise Stock Report"] = {
	"filters": [
		{
			"fieldname":"to_date",
			"label": __("Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.get_today(),
	},
	]
};
