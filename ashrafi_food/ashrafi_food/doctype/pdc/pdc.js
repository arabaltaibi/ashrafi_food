// Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('PDC', {
	refresh: function(frm) {
        if(frm.doc.docstatus==1 && frm.doc.clear==0){
			frm.add_custom_button("Create payment",function(){
				
				  frappe.call({
					  method:"ashrafi_food.ashrafi_food.doctype.pdc.pdc.create_payment",
					  args:{
						  doc:frm.doc.name
					  },
					 
					  callback:function(r){
						  if (r.message){
							   frappe.msgprint(`Payment entry created successfully`)
						  }
					  }
				  })
				
				
			})
		}

		frm.set_query('party_type', function(doc) {
		
			return {
				filters: {
					name: ["in",["Customer","Supplier"]]
				}
			};
		})

		frm.set_query("reference_doctype", "payment_entry_reference", function(doc, cdt, cdn) {
			let filters = []
			if (cur_frm.doc.party_type == "Customer"){
				filters = {
					"name":["in",["Sales Invoice"]],
				} 
			}
			if (cur_frm.doc.party_type == "Supplier"){
				filters = {
					"name":["in",["Purchase Invoice"]],
				} 
			}
			return {
				filters: filters
			}
		});

		frm.set_query("reference_name", "payment_entry_reference", function(doc, cdt, cdn) {
			let filters = []
			if (cur_frm.doc.party_type == "Customer"){
				filters = {
					"customer":cur_frm.doc.party
				} 
			}
			if (cur_frm.doc.party_type == "Supplier"){
				filters = {
					"supplier":cur_frm.doc.party
				} 
			}
			return {
				filters: filters
			}
		});
	},
	payment_type:function(frm){
		frm.set_value("party","")
		frm.clear_table("payment_entry_reference")
		frm.refresh()
	},
	party:function(frm){
		frm.clear_table("payment_entry_reference")
		frm.refresh()
	},
	get_data:function(frm){
		if(!frm.doc.amount_paid){
			frappe.msgprint("Please set amount paid")
			return false
		}
		var dialog = new frappe.ui.Dialog({
			title: __('Set Filters'),
			fields: [
	
				{ fieldtype: 'Date', reqd:1, fieldname: 'from_date', label: __("From Date") },
				{ fieldtype: 'Column Break' },
				{ fieldtype: 'Date',reqd:1, fieldname: 'to_date', label: __("To Date") },
				
			],
			primary_action: function () {
				var args = dialog.get_values();
				frappe.call({
					method:"ashrafi_food.ashrafi_food.doctype.pdc.pdc.get_data",
					args:{
						party_type:frm.doc.party_type,
						party:frm.doc.party,
						from_date:args.from_date,
						to_date:args.to_date
					},
				   
					callback:function(r){
						if (r.message){
							 //console.log(r.message)
							 let paid_amount = frm.doc.amount_paid
							 $.each(r.message, function(i, d) {
								if(paid_amount > 0){
									var c = frm.add_child("payment_entry_reference");
									c.reference_doctype = d.doctype;
									c.reference_name = d.name;
									c.total_amount = d.grand_total;
									c.outstanding_amount = d.outstanding_amount;
									c.payment_term = d.payment_terms_template
									if(paid_amount >= d.outstanding_amount){
										c.allocated_amount = d.outstanding_amount
									}
									else{
										c.allocated_amount =paid_amount
									}
									paid_amount = paid_amount - c.allocated_amount
									
								}
							 })
							 cur_frm.refresh_field("payment_entry_reference")
						}
					}
				})
			  
				dialog.hide()
			},
			primary_action_label: __("Submit")
		})
		dialog.show()
	}
});
