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
	conditions  = get_conditions(filters)
	DI = frappe.db.sql(
		"""select * from `tabDistributor Invoice` where %s """ 
		% conditions,
		filters,
		as_dict=1,
	)
	data = []
	for inv in DI:
		row = {
			"invoice_no":inv.get("name"),
			"shop_name":inv.get("customer_name"),
			"address":inv.get("customer_address"),
			"contact_person":inv.get("customer_contact_person"),
			"contact_number":inv.get("customer_contact_number"),
			"gross_amount":inv.get("total_amount"),
			"discount":inv.get("total_line_discount"),
			"bill_amount":inv.get("net_total_amount"),
			"balance_amount":inv.get("customer_balance"),
		}

		cash_amount  = frappe.db.get_value("Distributor Mode of Payment",
		             {"parent":inv.get("name"),"mode_of_payment":"Cash"},"sum(amount) as amount")
		cheque_amount  = frappe.db.get_value("Distributor Mode of Payment",
		             {"parent":inv.get("name"),"mode_of_payment":"Cheque"},"sum(amount) as amount")
		row.update({
			"cash_amount":cash_amount,
			"cheque_amount":cheque_amount,
			"cheque_no":frappe.db.get_value("Distributor Mode of Payment",
		             {"parent":inv.get("name"),"mode_of_payment":"Cheque"},"check_no"),
		    "cheque_date":frappe.db.get_value("Distributor Mode of Payment",
		             {"parent":inv.get("name"),"mode_of_payment":"Cheque"},"cheque_date"),

			"f10":frappe.db.get_value("Distribution Items",
		             {"parent":inv.get("name"),"item_code":"F10"},"sum(quantity) as qty"),
			"f05":frappe.db.get_value("Distribution Items",
		             {"parent":inv.get("name"),"item_code":"F05"},"sum(quantity) as qty"),
			"c10":frappe.db.get_value("Distribution Items",
		             {"parent":inv.get("name"),"item_code":"C10"},"sum(quantity) as qty"),
			"c05":frappe.db.get_value("Distribution Items",
		             {"parent":inv.get("name"),"item_code":"C05"},"sum(quantity) as qty"),
			"fl10":frappe.db.get_value("Distribution Items",
		             {"parent":inv.get("name"),"item_code":"FL10"},"sum(quantity) as qty"),
			"fl05":frappe.db.get_value("Distribution Items",
		             {"parent":inv.get("name"),"item_code":"FL05"},"sum(quantity) as qty")	
		})
		data.append(row)
	return data



def get_conditions(filters):
	conditions = " date between %(from_date)s and %(to_date)s and docstatus=1"
	if filters.get("sales_man"):
		conditions += " and sales_person = %(sales_man)s"
	if filters.get("vehicle"):
		conditions += " and vehicle_no = %(vehicle)s"
	if filters.get("area"):
		conditions += " and area = %(area)s"
	if filters.get("supervisor"):
		conditions += " and supervisor = %(supervisor)s"
	
	

	return conditions

def get_columns():
	columns = [
		{
			"label": _("INV#"),
			"fieldname": "invoice_no",
			"fieldtype": "Link",
			"options": "Distributor Invoice",
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
			"label": _("Gross Amount"),
			"fieldname": "gross_amount",
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
			"label": _("Bill Amount"),
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
			"label": _("Balance Amount"),
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


			
	]
	return columns
