from __future__ import unicode_literals
# import frappe

import frappe
from frappe.model.document import Document
import json
from frappe.utils import getdate, add_days, get_time,today
from frappe import _
import datetime
from frappe.core.doctype.sms_settings.sms_settings import send_sms
try:
    from erpnext.hr.doctype.employee.employee import is_holiday  # v13
except ImportError:
    from erpnext.setup.doctype.employee.employee import is_holiday  # v14/v15
from datetime import timedelta, datetime, date

class DistributorInvoice(Document):
	pass
	def validate(self):
		if self.mode_payment == "Credit":
			allow_credit = frappe.db.get_value('Customer', self.customer_name, 'allow_credit')
			if allow_credit == 0:
				frappe.throw("Customer is not allowed to sale on Credit Please Contact Superior to Allow")
			else:
				pass
		self.get_cus_address()
		self.get_cust_contact()
		self.set_customer_financials()
		enable_dis = frappe.db.get_single_value('Accounts Settings', 'enable_promotional_discount')
		if enable_dis == 1:
			if self.company == "Ashrafi Food Pvt. Ltd":
				self.set_af_promo()
		enable_prod_dis = frappe.db.get_single_value('Accounts Settings', 'enable_product_wise_discount')
		if enable_prod_dis == 1:
			if self.company == "Ashrafi Food Pvt. Ltd":
				self.set_af_prod_promo()
	def on_submit(self):
		self.create_si()
		self.set_payments()
		self.send_sms()
	def on_cancel(self):
		self.cancel_si()
	
	def send_sms(self):
		if not self.customer_mobile_no:
			return
		payment_mode = ''
		if self.is_cash_payment:
			payment_mode = "Cash"
		else:
			payment_mode = "Credit"
		number = str(self.customer_mobile_no)
		
		sms_text = """Thank you for your purchase from Ashrafi foods of amount {bill_amount} on {bill_date} in {payment_mode}

For complaints or order booking contact 03208288811
		""".format(bill_amount=self.net_total_amount,bill_date=self.date,payment_mode=payment_mode)
		send_sms([number],sms_text)
	def set_customer_financials(self):
		if not self.customer_name:
			self.outstanding_amount = 0
			self.last_invoice = 0
			return

		company = getattr(self, "company", None) or frappe.defaults.get_user_default("Company")

		# 1️⃣ Calculate outstanding from GL Entry
		res = frappe.db.sql("""
			SELECT IFNULL(SUM(debit) - SUM(credit), 0)
			FROM `tabGL Entry`
			WHERE party_type='Customer'
			  AND party=%s
			  AND company=%s
			  AND is_cancelled=0
		""", (self.customer_name, company))

		self.outstanding_amount = res[0][0] if res else 0

		# 2️⃣ Last posted Sales Invoice grand total
		last_invoice = frappe.get_all(
			"Sales Invoice",
			filters={
				"customer": self.customer_name,
				"company": company,
				"docstatus": 1
			},
			fields=["grand_total"],
			order_by="posting_date desc, creation desc",
			limit=1
		)

		self.last_invoice = last_invoice[0].grand_total if last_invoice else 0
	def set_af_promo(self):
		if self.promoted_customer == "Yes":
			total_promo_weight = 0
			for item in self.items:
				if item.if_promoted_item == "Yes" and item.item_code in ["C-05", "C-10", "F-05", "F-10"]:  # FL items removed
					tweight = item.weight_per_unit * item.quantity
					total_promo_weight += tweight

			self.discount_applicable_qty = total_promo_weight

			# Apply discount based on new scheme
			if 10 <= self.discount_applicable_qty <= 100:
				disc_perc = 2
			elif 120 <= self.discount_applicable_qty <= 250:
				disc_perc = 3
			elif 280 <= self.discount_applicable_qty <= 400:
				disc_perc = 4
			elif 450 <= self.discount_applicable_qty <= 750:
				disc_perc = 5
			elif self.discount_applicable_qty >= 800:
				disc_perc = 6
			else:
				disc_perc = 0

			self.prom_disc = disc_perc

			line_disc = 0
			total_amount = 0
			net_total_amount = 0
			for row in self.items:
				if row.if_promoted_item == "Yes" and row.item_code in ["C-05", "C-10", "F-05", "F-10"]:
					discount_val = row.actual_rate * self.prom_disc / 100
					row.l_discount = discount_val
					row.rate = row.actual_rate - discount_val
					row.amount = row.actual_rate * row.quantity
					row.net_total_amount = row.rate * row.quantity
					row.discount = row.amount - row.net_total_amount
				else:
					# No discount applied to FL items or non-promoted items
					row.l_discount = 0
					row.rate = row.actual_rate
					row.amount = row.actual_rate * row.quantity
					row.net_total_amount = row.amount
					row.discount = 0

				line_disc += row.discount
				total_amount += row.amount
				net_total_amount += row.net_total_amount

			self.total_line_discount = line_disc
			self.total_amount = total_amount
			self.net_total_amount = net_total_amount

	def set_af_prod_promo(self):
		if self.promoted_customer != "Yes":
			return

		# Reset counters from original code
		self.no_of_free_items = 0
		self.free_fl_item = 0
		total_promo_weight = 0
		total_fl_promo_weight = 0

		# Remove existing free items first (preserve your behavior)
		self.items = [row for row in self.items if row.is_free_item != 1]
		self.promoted_product_added = 0

		# Mapping: main item -> (free_item_code, free_item_name)
		free_map = {
			"F-10": ("PS - PINK SALT 800GM", "PS - PINK SALT 800GM"),
			"C-10": ("PS - PINK SALT 800GM", "PS - PINK SALT 800GM"),
			"F-05": ("TS - TABLE SALT 800GM", "TS - TABLE SALT 800GM"),
			"C-05": ("TS - TABLE SALT 800GM", "TS - TABLE SALT 800GM"),
		}

		free_items_count = {}  # {free_item_code: qty}

		# First pass: respect original checks and calculate totals
		for item in self.items:
			# preserve original allow_for_free_promotional_item check and skip free items
			allow_free = frappe.db.get_value('Item', item.item_code, 'allow_for_free_promotional_item')
			if item.if_promoted_item == "Yes" and allow_free == 1 and item.is_free_item != 1:
				# keep your promo weight behaviour for legacy logic
				if item.item_code in ["C10", "F10", "FL10","C05", "F05", "FL05"]:
					try:
						qty = float(item.quantity or 0)
						wpu = float(item.weight_per_unit or 0)
					except Exception:
						qty = item.quantity or 0
						wpu = item.weight_per_unit or 0
					total_promo_weight += wpu * qty

				# Count FL-specific promo if needed (kept for backward compatibility)
				if item.item_code.startswith("FL"):
					try:
						total_fl_promo_weight += (item.weight_per_unit or 0) * (item.quantity or 0)
					except Exception:
						pass

				# Apply new scheme mapping (1:1 free qty)
				if item.item_code in free_map:
					free_code, free_name = free_map[item.item_code]
					free_qty = item.quantity or 0

					if free_code not in free_items_count:
						free_items_count[free_code] = {"item_name": free_name, "qty": 0}
					free_items_count[free_code]["qty"] += free_qty

		# Set promo weight field(s) exactly like your original
		self.promo_weight = total_promo_weight

		# Optional: if you still want no_of_free_items to represent total free qty across all freebies
		self.no_of_free_items = sum([d["qty"] for d in free_items_count.values()]) if free_items_count else 0

		# Add computed free items as child rows
		if free_items_count:
			for free_code, data in free_items_count.items():
				ex = self.append("items")
				ex.item_code = free_code
				ex.item_name = data["item_name"]
				ex.quantity = data["qty"]
				ex.rate = 0
				# preserve your existing field names if you use actual_rate
				if hasattr(ex, "actual_rate"):
					ex.actual_rate = 0
				ex.is_free_item = 1

			self.promoted_product_added = 1

		# Debug prints similar to original code
		print(f"Total Promo Weight: {total_promo_weight}, No of Free Items: {self.no_of_free_items}")
		print(f"Total Flourio Promo Weight: {total_fl_promo_weight}, Free Flourio Item: {self.free_fl_item}")
		print("Free items added:", free_items_count)

		# If you rely on old weight-ranges logic to set no_of_free_items, you can re-enable it here:
		# weight_ranges = [(99, 200, 1), (199, 300, 2), ...]
		# (kept out for clarity since your new scheme is 1:1)




	def get_cus_address(self):
		cust_address = frappe.db.get_value('Address', {'customer': self.customer_name}, ['name'])
		if cust_address:
			address = frappe.get_doc("Address", cust_address)
			if address.address_line1:
				line1 = address.address_line1
			else:
				line1 = ""
			if address.address_line2:
				line2 = address.address_line2
			else:
				line2 = ""
			if address.city:
				city = address.city
			else:
				city = ""
			if address.state:
				state = address.state
			else:
				state = ""
			self.customer_address = line1 + ", " + line2 + ", " + city + ", " + state
		else:
			self.customer_address = ""
	def get_cust_contact(self):
		if self.customer_contact_person:
			contact = frappe.get_doc("Contact", self.customer_contact_person)
			if contact.first_name:
				first_name = contact.first_name
			else:
				first_name = ""
			if contact.last_name:
				last_name = contact.last_name
			else:
				last_name = ""
			if contact.mobile_no:
				mobile = contact.mobile_no
			else:
				mobile = ""
			if contact.phone:
				phone = contact.phone
			else:
				phone = ""
			self.contact_detail = "First Name: " + first_name + "\nLast Name: " + last_name + "\nMobile No: " + mobile + "\nPhone: " + phone
		else:
			pass
	def create_si(self):
		if len(self.items) == 0:
			return True
		if self.sales_type == "Sales":
			si = frappe.new_doc('Sales Invoice')
			si.customer = self.customer_name
			si.set_posting_time = 1
			si.posting_date = self.date
			si.distributor_invoice_no = self.name
			si.bill_no = self.bill_no
			si.bill_picture = self.bill_picture
			si.update_stock = 1
			si.set_warehouse = self.warehouse
			si.gross_total = self.net_total_amount
			for items in self.items:
				sii = si.append("items")
				sii.item_code = items.item_code
				sii.qty = items.quantity
				sii.rate = items.rate
				sii.total_discount = items.discount
				sii.l_discount = items.l_discount
				sii.discount_amount = 	items.discount
				if sii.rate == 0:
					sii.discount_percentage = 	100
			si.save()
			self.sales_invoice_ref = ""
			self.sales_invoice_ref = si.name
			self.save()
			si.submit()
		else:
			si = frappe.new_doc('Sales Invoice')
			si.is_return = 1
			si.customer = self.customer_name
			si.set_posting_time = 1
			si.posting_date = self.date
			si.distributor_invoice_no = self.name
			si.bill_no = self.bill_no
			si.bill_picture = self.bill_picture
			si.update_stock = 1
			si.set_warehouse = self.warehouse
			si.gross_total = self.net_total_amount
			for items in self.items:
				sii = si.append("items")
				sim = "-"
				sii.item_code = items.item_code
				sii.qty = items.quantity
				sii.rate = items.rate
				sii.total_discount = items.discount
				sii.discount_amount = 	items.discount
				if sii.rate == 0:
					sii.discount_percentage = 	100
			si.save()
			if self.sales_invoice_ref:
				self.sales_invoice_ref = ""
			self.sales_invoice_ref = si.name
			self.save()
			si.submit()

	def cancel_si(self):
		if self.sales_invoice_ref:
			si = frappe.get_doc("Sales Invoice", self.sales_invoice_ref)
			si.cancel()
		else:
			pass
	def set_payments(self):
		if self.mode_of_payment:
			pe = frappe.new_doc("Payment Entry")
			pe.payment_type = "Receive"
			pe.posting_date = self.date
			pe.mode_of_payment = self.mode_of_payment
			pe.party_type = "Customer"
			pe.party = self.customer_name
			pe.paid_from = "1310 - Debtors - AFI"
			pe.paid_to = frappe.db.get_value("Mode of Payment Account",{"parent":self.mode_of_payment},"default_account") or "1110 - Cash - AFI"
			pe.paid_amount = self.amount
			pe.received_amount = self.amount
			for invoices in self.distributor_payment:
				ref = pe.append("references")
				ref.reference_doctype = "Sales Invoice"
				ref.reference_name = invoices.invoice_no
				ref.allocated_amount = invoices.allocated
				pe.insert()
				invoices.payment_ref = pe.name
				self.save()
			frappe.msgprint("Cash Payment Created")
		if self.bank_mode_of_payment:
			pe = frappe.new_doc("Payment Entry")
			pe.payment_type = "Receive"
			pe.posting_date = self.date
			pe.mode_of_payment = self.bank_mode_of_payment
			pe.party_type = "Customer"
			pe.party = self.customer_name
			pe.paid_from = "1310 - Debtors - AFI"
			pe.paid_to = frappe.db.get_value("Mode of Payment Account",{"parent":self.bank_mode_of_payment},"default_account") or "Bank - AFI"
			pe.paid_amount = self.bank_amount
			pe.received_amount = self.bank_amount
			for invoices in self.payment:
				ref = pe.append("references")
				ref.reference_doctype = "Sales Invoice"
				ref.reference_name = invoices.invoice_no
				ref.allocated_amount = invoices.allocated
				pe.insert()
				invoices.payment_ref = pe.name
				self.save()
			frappe.msgprint("Bank Payment Created")
@frappe.whitelist()
def your_custom_method_to_get_unpaid_invoices(customer):
	invoices = frappe.db.sql("""
	SELECT name as invoice_no, grand_total as invoice_amount
	FROM `tabSales Invoice`
	WHERE customer = %s AND outstanding_amount > 0
	""", (customer), as_dict=True)
	return invoices
