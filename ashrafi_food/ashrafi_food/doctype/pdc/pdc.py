# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PDC(Document):
	pass

@frappe.whitelist()
def create_payment(doc):
	data = frappe.get_doc("PDC",doc)
	pe = frappe.new_doc("Payment Entry")
	pe.posting_date = data.posting_date
	pe.payment_type = data.payment_type
	pe.mode_of_payment = data.mode_of_payment or "Cheque"
	pe.party_type = data.party_type
	pe.party = data.party
	pe.reference_no = data.cheque_number
	pe.reference_date = data.cheque_date
	pe.source_exchange_rate = 1
	pe.target_exchange_rate = 1
	pe.bill_type = "Current Bill"
	total_paid = 0
	for d in data.payment_entry_reference:
		pe.append("references",{
			 "reference_name":d.reference_name,
			"reference_doctype": d.reference_doctype,
			"total_amount": d.total_amount,
			"outstanding_amount": d.outstanding_amount,
			"allocated_amount": d.allocated_amount,
			"exchange_rate":1,
			"payment_term":d.payment_term
		})
		total_paid += d.allocated_amount
	pe.paid_amount = total_paid,
	pe.paid_amount_after_tax = total_paid
	pe.received_amount = total_paid
	if pe.payment_type == "Receive":
		pe.paid_to = data.link_7
	else:
		pe.paid_from = data.link_7
	pe.save()
	pe = frappe.get_doc("Payment Entry",pe.name)
	pe.update({
		"paid_amount":total_paid,
		"received_amount":total_paid
	})
	pe.save()
	data.db_set("clear",1)
	return True

@frappe.whitelist()	
def get_data(party_type,party,from_date,to_date):
	doctype = "Purchase Invoice"
	filters = {
		"posting_date":("between",[from_date,to_date]),
		"docstatus":1,
		"outstanding_amount":["!=",0],
		"supplier":party
	}
	if party_type == "Customer":
		doctype = "Sales Invoice"
		filters["customer"]=party
		del filters["supplier"]
	data = frappe.db.get_all(doctype,filters=filters,fields=["name","grand_total","outstanding_amount","payment_terms_template"],order_by="posting_date ASC")
	for d in data:
		if not d.payment_terms_template:
			d.payment_terms_template = frappe.db.get_value(party_type,party,"payment_terms")
		d.doctype = "Sales Invoice" if party_type == "Customer" else "Purchase Invoice"
	return data