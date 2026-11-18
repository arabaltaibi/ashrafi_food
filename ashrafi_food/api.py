import frappe


@frappe.whitelist()
def get_unpaid_invoices(customer):
    return frappe.db.sql(
        """select name as invoice_no, grand_total as invoice_amount
           from `tabSales Invoice`
           where customer = %s and outstanding_amount > 0""",
        (customer,),
        as_dict=True,
    )
