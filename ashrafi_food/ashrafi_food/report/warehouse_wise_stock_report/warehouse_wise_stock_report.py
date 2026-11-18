# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _, _dict
from frappe.utils import today

def execute(filters=None):
	if not filters:
		filters = {}
	
	# Fallback if the user hasn't selected a date filter yet
	if not filters.get("to_date"):
		filters["to_date"] = today()

	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_data(filters):
	data = []
	WHS = frappe.db.get_all("Warehouse", filters={"is_group": 0}, fields=["name"])
	to_date = filters.get("to_date")

	# Define exact mapping from Item Code -> Column fieldname
	item_map = {
		"F-10": "f-10",
		"F-05": "f-05",
		"C-10": "c-10",
		"C-05": "c-05",
		"FL-10": "fl-10",
		"FL-05": "fl-05",
		"SF-10": "sf-10",
		"SF-05": "sf-05",
		"FLOUR [50-KG PACKING]": "sf-50"
	}

	for wh in WHS:
		row = {
			"warehouse": wh.name,
		}
		total_qty = 0
		
		for item_code, fieldname in item_map.items():
			act_qty = get_balance_qty_from_sle(item_code, wh.name, to_date)
			row.update({
				fieldname: act_qty
			})
			total_qty += act_qty
			
		row.update({"total": total_qty})
		data.append(row)

	return data


def get_balance_qty_from_sle(item_code, warehouse, posting_date):
	if not posting_date:
		return 0.0

	balance_qty = frappe.db.sql("""
		select qty_after_transaction from `tabStock Ledger Entry`
		where item_code=%s and warehouse=%s and is_cancelled='No' and posting_date <= %s
		order by posting_date desc, posting_time desc, creation desc
		limit 1
	""", (item_code, warehouse, posting_date))

	return float(balance_qty[0][0]) if balance_qty else 0.0


def get_columns():
	return [
		{
			"label": _("Warehouse"),
			"fieldname": "warehouse",
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 300
		},
		{
			"label": _("F-10"),
			"fieldname": "f-10",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("F-05"),
			"fieldname": "f-05",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("C-10"),
			"fieldname": "c-10",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("C-05"),
			"fieldname": "c-05",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("FL-10"),
			"fieldname": "fl-10",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("FL-05"),
			"fieldname": "fl-05",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("SF-10"),
			"fieldname": "sf-10",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("SF-05"),
			"fieldname": "sf-05",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("FLOUR [50-KG PACKING]"),
			"fieldname": "sf-50",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("Total"),
			"fieldname": "total",
			"fieldtype": "Float",
			"width": 100,
		},
	]