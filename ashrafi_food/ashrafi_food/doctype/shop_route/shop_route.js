// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Shop Route', {
	master_shop_route: function(frm) {
		frm.doc.table_2 = [];
		erpnext.utils.map_current_doc({
			method: "ashrafi_food.ashrafi_food.doctype.shop_route.shop_route.fetch_appraisal_template",
			source_name: frm.doc.master_shop_route,
			frm: frm
		});
	},
});
