// Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Distributor Invoice', {
	
	refresh: function(frm) {
      if(frm.doc.__islocal && !frm.doc.warehouse){
		frappe.db.get_value("User", {"name": frappe.session.user}, 
		        "warehouse", (r) => {
			frm.set_value("warehouse",r.warehouse)
		});
	  }
	}
});
