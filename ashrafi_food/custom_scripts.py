import frappe
from frappe.utils import nowdate
@frappe.whitelist()
def generate_sales_invoices(delivery_notes):
    if isinstance(delivery_notes, str):
        import json
        delivery_notes = json.loads(delivery_notes)

    created_invoices = []

    for dn_name in delivery_notes:
        dn = frappe.get_doc("Delivery Note", dn_name)

        if dn.status != "To Bill":
            frappe.msgprint(f"Skipping {dn_name}: Already Billed or Canceled")
            continue
        
        # Create Sales Invoice
        invoice = frappe.new_doc("Sales Invoice")
        invoice.customer = dn.customer
        invoice.posting_date = dn.posting_date
        invoice.due_date = dn.posting_date
        invoice.set_posting_time = 1
        invoice.debit_to = frappe.get_value("Company", dn.company, "default_receivable_account")
        invoice.company = dn.company
        invoice.project = dn.project
        invoice.is_pos = 0
        invoice.items = []

        # Add Items from Delivery Note
        for item in dn.items:
            invoice.append("items", {
                "item_code": item.item_code,
                "qty": item.qty,
                "rate": item.rate,
                "delivery_note": dn.name,
                "warehouse": item.warehouse,
                "delivered_qty": item.qty
            })

        invoice.save()
        invoice.submit()
        created_invoices.append(invoice.name)
        frappe.db.set_value("Delivery Note", dn_name, "per_billed", 100)
        frappe.db.set_value("Delivery Note", dn_name, "status", "Completed")

        # Mark Delivery Note as Billed

    return {"invoices": created_invoices}
@frappe.whitelist()
def generate_purchase_invoices(purchase_receipts):
    if isinstance(purchase_receipts, str):
        import json
        purchase_receipts = json.loads(purchase_receipts)

    created_invoices = []

    for pr_name in purchase_receipts:
        pr = frappe.get_doc("Purchase Receipt", pr_name)

        if pr.status != "To Bill":
            frappe.msgprint(f"Skipping {pr_name}: Already Billed or Canceled")
            continue
        
        # Create Purchase Invoice
        invoice = frappe.new_doc("Purchase Invoice")
        invoice.supplier = pr.supplier
        invoice.posting_date = pr.posting_date
        invoice.due_date = pr.posting_date
        invoice.set_posting_time = 1
        invoice.credit_to = frappe.get_value("Company", pr.company, "default_payable_account")
        invoice.company = pr.company
        invoice.items = []

        # Add Items from Purchase Receipt
        for item in pr.items:
            invoice.append("items", {
                "item_code": item.item_code,
                "qty": item.qty,
                "rate": item.rate,
                "purchase_receipt": pr.name,
                "warehouse": item.warehouse,
                "received_qty": item.qty
            })

        invoice.save()
        invoice.submit()
        created_invoices.append(invoice.name)
        
        # Update Purchase Receipt as Billed
        frappe.db.set_value("Purchase Receipt", pr_name, "per_billed", 100)

    return {"invoices": created_invoices}



@frappe.whitelist()
def get_customer_financials(customer, company=None):
    data = {
        "outstanding_amount": 0,
        "last_invoice_total": 0
    }

    if not customer:
        return data

    company = company or frappe.defaults.get_user_default("Company")

    # 1️⃣ Customer Outstanding (from GL Entry)
    outstanding = frappe.db.sql("""
        SELECT
            SUM(debit - credit)
        FROM `tabGL Entry`
        WHERE
            party_type = 'Customer'
            AND party = %s
            AND company = %s
            AND is_cancelled = 0
    """, (customer, company))[0][0]

    data["outstanding_amount"] = outstanding or 0

    # 2️⃣ Last Sales Invoice Grand Total
    last_invoice = frappe.get_all(
        "Sales Invoice",
        filters={
            "customer": customer,
            "company": company,
            "docstatus": 1
        },
        fields=["grand_total"],
        order_by="posting_date desc, creation desc",
        limit=1
    )

    if last_invoice:
        data["last_invoice_total"] = last_invoice[0].grand_total

    return data
