# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _, _dict
from frappe.utils import cstr, getdate
from six import iteritems

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_data(filters):
	try:
		conditions  = get_conditions(filters)
		DI = frappe.db.sql(
			"""select * from `tabSales Invoice` where %s """ 
			% conditions,
			filters,
			as_dict=1,
		)
		data = []
		for inv in DI:
			disc_amnt = (frappe.db.get_all("Sales Invoice Item",
						filters={"parent":inv.get("name")},fields=["sum(total_discount) as discount"])[0].get("discount",0) or 0)
			row = {
				"invoice_no":inv.get("name"),
				"shop_name":inv.get("customer_name"),
				"address":inv.get("address_display"),
				"contact_person":inv.get("contact_person"),
				"contact_number":frappe.db.get_value("Customer",{"name":inv.get("customer")},"customer_mobile_no") or "",
				"gross_amount":inv.get("grand_total") + disc_amnt,#inv.get("gross_total"),
				"discount_per_unit":(frappe.db.get_all("Sales Invoice Item",
						filters={"parent":inv.get("name")},fields=["sum(l_discount) as discount_per_unit"])[0].get("discount_per_unit",0) or 0),
				"discount":disc_amnt,
				"bill_amount":inv.get("grand_total"),
				"bill_no":inv.get("bill_no"),
				"balance_amount":inv.get("outstanding_amount"),
				"sales_man":inv.get("owner"),
				"full_name":frappe.db.get_value("User",{"name":inv.get("owner")},"full_name") or "",
				"posting_time":inv.get("posting_time"),
				"posting_date":inv.get("posting_date"),
				"attachement":"""<a href="https://af.tboss.info{0}"> {1} </a>""".format(frappe.db.get_value("Distributor Invoice",{"sales_invoice_ref":inv.get("name")},"attach_image") or "",frappe.db.get_value("Distributor Invoice",{"sales_invoice_ref":inv.get("name")},"attach_image") or "")
			}
			# (frappe.db.get_all("Sales Invoice Item",
			# 			filters={"parent":inv.get("name")},fields=["sum(discount_amount) as discount"])[0].get("discount",0) or 0)+

			cash_amount  = frappe.db.sql(""" select p.name, p.mode_of_payment,reference_no,reference_date, sum(pr.allocated_amount) as cash_amount
										from `tabPayment Entry` p
											LEFT JOIN `tabPayment Entry Reference` pr
											ON pr.parent=p.name
											where pr.reference_name=%s and pr.reference_doctype="Sales Invoice"
											and p.mode_of_payment in 
											(select name from `tabMode of Payment` where type='Cash')
											and p.docstatus=1 
											""",(inv.get("name")),as_dict=1)
			cheque_amount  = frappe.db.sql(""" select p.name, p.mode_of_payment,reference_no,reference_date, sum(pr.allocated_amount) as bank_amount
										from `tabPayment Entry` p
											LEFT JOIN `tabPayment Entry Reference` pr
											ON pr.parent=p.name
											where pr.reference_name=%s and pr.reference_doctype="Sales Invoice"
											and p.mode_of_payment in 
											(select name from `tabMode of Payment` where type='Bank')
											and p.docstatus=1 
											""",(inv.get("name")),as_dict=1)
			row.update({
				"cash_amount":cash_amount[0]['cash_amount'] or 0,
				"cheque_amount":cheque_amount[0]['bank_amount'] or 0,
				"cheque_no":cheque_amount[0]['reference_no'] or 0,
				"cheque_date":cheque_amount[0]['reference_date'] or 0,

				"f10":frappe.db.get_value("Sales Invoice Item",
						{"parent":inv.get("name"),"item_code":"F-10"},"sum(qty) as qty"),
				"f05":frappe.db.get_value("Sales Invoice Item",
						{"parent":inv.get("name"),"item_code":"F-05"},"sum(qty) as qty"),
				"c10":frappe.db.get_value("Sales Invoice Item",
						{"parent":inv.get("name"),"item_code":"C-10"},"sum(qty) as qty"),
				"c05":frappe.db.get_value("Sales Invoice Item",
						{"parent":inv.get("name"),"item_code":"C-05"},"sum(qty) as qty"),
				"fl10":frappe.db.get_value("Sales Invoice Item",
						{"parent":inv.get("name"),"item_code":"FL-10"},"sum(qty) as qty"),
				"fl05":frappe.db.get_value("Sales Invoice Item",
						{"parent":inv.get("name"),"item_code":"FL-05"},"sum(qty) as qty"),
				"sf10":frappe.db.get_value("Sales Invoice Item",
						{"parent":inv.get("name"),"item_code":"SF-10"},"sum(qty) as qty"),
				"sf05":frappe.db.get_value("Sales Invoice Item",
						{"parent":inv.get("name"),"item_code":"SF-05"},"sum(qty) as qty"),
				"ps":frappe.db.get_value("Sales Invoice Item",
						{"parent":inv.get("name"),"item_code":"PS - PINK SALT 800GM"},"sum(qty) as qty"),
				"ts":frappe.db.get_value("Sales Invoice Item",
						{"parent":inv.get("name"),"item_code":"TS - TABLE SALT 800GM"},"sum(qty) as qty")
					
			})
			data.append(row)
	except:
		frappe.log_error(frappe.get_traceback(),"DSA R")
	
	return data



def get_conditions(filters):
	conditions = " posting_date between %(from_date)s and %(to_date)s and docstatus=1"
	if filters.get("sales_man"):
		conditions += " and owner = %(sales_man)s"
	if filters.get("vehicle"):
		conditions += " and vehicle_no = %(vehicle)s"
	if filters.get("area"):
		conditions += " and territory = %(area)s"
	if filters.get("supervisor"):
		conditions += " and supervisor = %(supervisor)s"
	
	

	return conditions

def get_columns():
	columns = [
		{
			"label": _("Posting Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
		},
		{
			"label": _("Posting Time"),
			"fieldname": "posting_time",
			"fieldtype": "Time",
		},
		{
			"label": _("INV#"),
			"fieldname": "invoice_no",
			"fieldtype": "Link",
			"options": "Sales Invoice",
		},
		{
			"label": _("Sales Man"),
			"fieldname": "full_name",
			"fieldtype": "Data",
		},
		{"label": _("Shop Name"), "fieldname": "shop_name", "fieldtype": "Data", "width": 150},
		{
			"label": _("Address"),
			"fieldname": "address",
			"fieldtype": "Data",
			"width": 300,
		},
		
		{"label": _("Contact Person"), "fieldname": "contact_person","fieldtype": "Data", "width": 200},
		{"label": _("Contact No."), "fieldname": "contact_number","fieldtype": "Data" ,"width": 200},

		{
			"label": _("F10"),
			"fieldname": "f10",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("F05"),
			"fieldname": "f05",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("C10"),
			"fieldname": "c10",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("C05"),
			"fieldname": "c05",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("FL10"),
			"fieldname": "fl10",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("FL05"),
			"fieldname": "fl05",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("SF10"),
			"fieldname": "sf10",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("SF05"),
			"fieldname": "sf05",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("PS"),
			"fieldname": "ps",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("TS"),
			"fieldname": "ts",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("Gross Amount"),
			"fieldname": "gross_amount",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("Discount per Unit"),
			"fieldname": "discount_per_unit",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("Discount"),
			"fieldname": "discount",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("Bill No"),
			"fieldname": "bill_no",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("Net Amount"),
			"fieldname": "bill_amount",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("Cash Amount"),
			"fieldname": "cash_amount",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("Cheuqe Amount"),
			"fieldname": "cheque_amount",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("Bill Balance"),
			"fieldname": "balance_amount",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("ChQ#"),
			"fieldname": "cheque_no",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("CHQ Date"),
			"fieldname": "cheque_date",
			"fieldtype": "Date",
			"width": 100,
		},
		
		{
			"label": _("Attachment"),
			"fieldname": "attachement",
			"fieldtype": "Data",
			"width": 100,
		},


			
	]
	return columns
