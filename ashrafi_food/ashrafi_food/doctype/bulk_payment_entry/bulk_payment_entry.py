# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class BulkPaymentEntry(Document):
	pass
	def on_submit(self):
		self.create_pi()
	def create_pi(self):
		for row in self.payment:
			doc = frappe.new_doc("Payment Entry")
			doc.posting_date = self.date
			if row.party_type == "Supplier":
				doc.payment_type = "Pay"
			else:
				doc.payment_type = "Receive"
			doc.party_type = row.party_type
			doc.party = row.party
			doc.mode_of_payment = row.mode_of_payment
			doc.bill_type = "Advance payment"
			payment_account = None
			pydoc = frappe.get_doc("Mode of Payment", row.mode_of_payment)
			for mop in pydoc.accounts:
				if mop.company == "Ashrafi Food Pvt. Ltd":
					payment_account = mop.default_account
			if row.party_type == "Supplier":
				doc.paid_from = payment_account
				doc.paid_to = "2110 - Sundries Creditors - AFI"
				doc.paid_amount = row.paid_amount
			if row.party_type == "Customer":
				doc.paid_to = payment_account
				doc.paid_from = "1310 - Sundry Debtors - AFI"
				doc.paid_amount = row.paid_amount				
			doc.reference_no  = row.ref_no
			doc.reference_date = row.ref_date
			doc.received_amount = row.paid_amount
			doc.target_exchange_rate = 1
			doc.source_exchange_rate = 1
			doc.paid_to_account_currency = "PKR"
			doc.paid_from_account_currency = "PKR"
			doc.save()
			doc.submit()
