frappe.ui.form.on("Payment Entry", {
    refresh(frm) {
        // ERPNext v13 already has this button inside its own code
        const major = parseInt((((frappe.boot || {}).versions || {}).erpnext || "0").split(".")[0]);
        if (major < 14) return;
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__("Create Reversal Entry"), () => {
                frappe.call({
                    method: "ashrafi_food.overrides.payment_entry.create_reversal",
                    args: { docname: frm.doc.name },
                    freeze: true,
                    callback: () => {
                        frappe.msgprint(__("Reversal Entry Created, Please refresh the Page!"));
                    },
                });
            });
        }
    },
});
