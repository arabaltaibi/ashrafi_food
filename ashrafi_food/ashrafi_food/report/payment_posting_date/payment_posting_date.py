# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def get_columns():
	return [
		"ID:Link/Payment Entry:220",
		"Posting Date:Date:100",
		"Party:Data:100",
		"Address:Data:220",
		"Contact No:Data:100",
		"Bill No.:Data:100",
		"Bill Amount:Float:150",
		"Bill Date:Date:200",
		"Bill:Data:150",
		"Area:Link/Territory:220",
		"Received Amount:Float:100",
		"Mode Of Payment:Link/Mode of Payment:100",
		"Cheque#:Data:100",
		"Cheque Date:Date:100",
		"Balance Amount:Float:100",
		"Payment Created By:Data:100"
	]
def get_data(filters):
		try:
			condition = ""
			#if filters.get("territory"):
			#	condition += " and co.territory = '{0}'".format(filters.get("territory"))
			if filters.get("sales_person"):
				condition += " and si.name in ( select sales_invoice_ref from `tabDistributor Invoice` where sales_person='{0}')".format(filters.get("sales_person"))
			if filters.get("mode_of_payment"):
				condition += " and pe.mode_of_payment = '{0}'".format(filters.get("mode_of_payment"))
				

			data = []
			res = frappe.db.sql("""
			SELECT
				pe.name ,
				pe.posting_date ,
				pe.party_name ,
				co.primary_address ,
				per.bill_no ,
				per.total_amount ,
				per.due_date ,
				pe.bill_type,
				si.territory,
				per.allocated_amount ,
				pe.mode_of_payment ,
				pe.reference_no ,
				pe.reference_date,
				per.outstanding_amount,
				co.customer_mobile_no,
				pe.owner
			
			
				FROM
					`tabPayment Entry` AS pe
				LEFT JOIN
					`tabPayment Entry Reference` AS per ON per.parent = pe.name
				LEFT JOIN
					`tabCustomer` AS co ON co.name = pe.party_name
				LEFT JOIN
					`tabSales Invoice` AS si ON si.name = per.reference_name
					
				WHERE
					pe.docstatus = 1
					and pe.posting_date >= %s and pe.posting_date <= %s
					{condition}
					and pe.bill_type <> "Current Bill"
					""".format(condition=condition),
					(filters.get("from_date"),filters.get("to_date"))
					,as_dict=1)
			for r in res:
				
				data.append([
					r["name"],
					r["posting_date"],
					r["party_name"],
					r["primary_address"],
					r["customer_mobile_no"],
					r["bill_no"],
					r["total_amount"],
					r["due_date"],
					r["bill_type"],
					r["territory"],
					r["allocated_amount"],
					r["mode_of_payment"],
					r["reference_no"],
					r["reference_date"],
					r["outstanding_amount"],
					r["owner"]
					
				])
			return data
		except:
			frappe.log_error(frappe.get_traceback(),"REP")
