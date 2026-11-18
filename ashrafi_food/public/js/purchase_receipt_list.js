frappe.listview_settings['Purchase Receipt'] = {
	add_fields: ["supplier", "supplier_name", "base_grand_total", "is_subcontracted",
		"transporter_name", "is_return", "status", "per_billed", "currency"],
	get_indicator: function(doc) {
		if(cint(doc.is_return)==1) {
			return [__("Return"), "gray", "is_return,=,Yes"];
		} else if (doc.status === "Closed") {
			return [__("Closed"), "green", "status,=,Closed"];
		} else if (flt(doc.per_returned, 2) === 100) {
			return [__("Return Issued"), "grey", "per_returned,=,100"];
		} else if (flt(doc.grand_total) !== 0 && flt(doc.per_billed, 2) < 100) {
			return [__("To Bill"), "orange", "per_billed,<,100"];
		} else if (flt(doc.grand_total) === 0 || flt(doc.per_billed, 2) === 100) {
			return [__("Completed"), "green", "per_billed,=,100"];
		}
	},
    refresh: function (listview) {
        listview.page.add_inner_button(__('Generate Invoices'), function () {
            let selected_docs = listview.get_checked_items();

            if (selected_docs.length === 0) {
                frappe.msgprint(__('Please select at least one Purchase Receipt.'));
                return;
            }

            let pr_names = selected_docs.map(doc => doc.name);

            frappe.call({
                method: "ashrafi_food.custom_scripts.generate_purchase_invoices",
                args: { purchase_receipts: pr_names },
                callback: function (r) {
                    if (!r.exc) {
                        frappe.msgprint(__('Purchase Invoices Created Successfully!'));
                        listview.refresh();
                    }
                }
            });
        });
    }
};
