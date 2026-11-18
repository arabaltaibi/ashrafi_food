// Copyright (c) 2020, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('FG Production Order', {
	finished_good: function(frm) {
		get_items(frm);	
	},
	qty:function(frm){
		get_items(frm);
	},

  setup: function(frm) {
    frm.set_query("target_warehouse", function() {
      return {
        filters: [
          ["Warehouse","company", "in", frm.doc.company]
        ]
      }
    });
  }
});


function get_items(frm){
	if(frm.doc.finished_good && frm.doc.qty){
		frappe.call({method:'get_items', doc:frm.doc, callback:function(r){frm.refresh_field('items')}});
	}
}


cur_frm.set_query("finished_good", function() {
	return {
		"filters": {
			
			"docstatus": 1
		}
	}
})
