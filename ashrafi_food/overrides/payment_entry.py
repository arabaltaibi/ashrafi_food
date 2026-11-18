import frappe
from frappe.core.doctype.sms_settings.sms_settings import send_sms
from frappe.utils import fmt_money

from ashrafi_food.overrides import ACTIVE


def on_submit(doc, method=None):
    if not ACTIVE:
        return
    if doc.get("bill_type") != "Recovery":
        return
    if not doc.get("phone_no"):
        frappe.msgprint("Could not send SMS due to missing phone number.")
        return
    msg = " Thankyou to give recovery to Mr. {0} {1} as a {2}".format(
        doc.get("user_name"), fmt_money(doc.paid_amount), doc.mode_of_payment
    )
    if doc.mode_of_payment == "Cheque":
        msg += " dated {0}. Cheque No. {1}.For complaint & booking contact 0320-8288811 ".format(
            doc.reference_date, doc.reference_no
        )
    send_sms([str(doc.phone_no)], msg)


@frappe.whitelist()
def create_reversal(docname):
    doc = frappe.get_doc("Payment Entry", docname)

    # reversal entry
    jv = frappe.new_doc("Journal Entry")
    jv.voucher_type = "Journal Entry"
    jv.company = doc.company
    jv.posting_date = doc.reference_date
    jv.cheque_no = doc.reference_no
    jv.cheque_date = doc.reference_date
    jv.user_remark = "Cheque Reversal Entry"
    jv.reversal_entry_link = doc.name
    deb = jv.append("accounts")
    deb.account = doc.paid_from
    deb.party_type = doc.party_type
    deb.party = doc.party
    deb.debit_in_account_currency = doc.paid_amount
    cre = jv.append("accounts")
    cre.account = doc.paid_to
    cre.credit_in_account_currency = doc.paid_amount
    jv.save()
    jv.submit()

    # main entry
    me = frappe.new_doc("Journal Entry")
    me.voucher_type = "Journal Entry"
    me.company = doc.company
    me.posting_date = doc.reference_date
    me.cheque_no = doc.reference_no
    me.cheque_date = doc.reference_date
    me.user_remark = "Main entry amended from " + doc.name
    me.reversal_entry_link = doc.name
    cre = me.append("accounts")
    cre.account = doc.paid_from
    cre.party_type = doc.party_type
    cre.party = doc.party
    cre.credit_in_account_currency = doc.paid_amount
    deb = me.append("accounts")
    deb.account = doc.paid_to
    deb.debit_in_account_currency = doc.paid_amount
    me.save()
    me.submit()

    doc.cancel()
