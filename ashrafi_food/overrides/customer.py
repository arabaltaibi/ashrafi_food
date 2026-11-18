import frappe

from ashrafi_food.overrides import ACTIVE


def on_update(doc, method=None):
    if not ACTIVE:
        return
    if doc.flags.is_new_doc and doc.get("customer_primary_address") and not doc.get("address_link"):
        doc.db_set("address_link", doc.customer_primary_address, update_modified=False)
        if frappe.get_meta("Address").has_field("customer"):
            frappe.db.set_value("Address", doc.customer_primary_address, "customer", doc.name, update_modified=False)
