import frappe
from frappe import _

from ashrafi_food.overrides import ACTIVE


def _make_jv(si, credit_field, debit_field, debit_party_type=None, debit_party=None):
    jv = frappe.new_doc("Journal Entry")
    jv.voucher_type = "Journal Entry"
    jv.posting_date = si.posting_date
    jv.company = si.company
    cr = jv.append("accounts")
    cr.account = frappe.db.get_value("Company", si.company, credit_field)
    cr.party_type = "Customer"
    cr.party = si.customer
    cr.credit_in_account_currency = si.grand_total
    dr = jv.append("accounts")
    dr.account = frappe.db.get_value("Company", si.company, debit_field)
    if debit_party_type:
        dr.party_type = debit_party_type
        dr.party = debit_party
    dr.debit_in_account_currency = si.grand_total
    jv.save()
    jv.submit()
    si.db_set("jv", jv.name)


def on_submit(doc, method=None):
    if not ACTIVE:
        return
    if doc.get("free_sample"):
        _make_jv(doc, "free_credit_account", "free_debit_account")
    if doc.get("emp_paid"):
        _make_jv(doc, "emp_credit_account", "emp_debit_account", "Employee", doc.get("employee"))


def before_cancel(doc, method=None):
    if not ACTIVE:
        return
    # 1. cancel the free-sample / employee-paid Journal Entry
    if doc.get("jv") and frappe.db.get_value("Journal Entry", doc.jv, "docstatus") == 1:
        frappe.get_doc("Journal Entry", doc.jv).cancel()
        frappe.msgprint(_("Journal Entry {0} has been cancelled.").format(doc.jv))
    # 2. cancel submitted Payment Entries made against this invoice
    payment_entries = frappe.db.sql_list(
        """select distinct t1.name
           from `tabPayment Entry` t1, `tabPayment Entry Reference` t2
           where t1.name = t2.parent and t1.docstatus = 1 and t2.reference_name = %s""",
        doc.name,
    )
    for pe in payment_entries:
        frappe.get_doc("Payment Entry", pe).cancel()
