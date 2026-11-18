# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, getdate

from erpnext.hr.utils import set_employee_name, validate_active_employee

class ShopRoute(Document):
	pass
@frappe.whitelist()
def fetch_appraisal_template(source_name, target_doc=None):
	target_doc = get_mapped_doc(
		"Master Shop Route",
		source_name,
		{
			"Master Shop Route": {
				"doctype": "Shop Route",
			},
			"Shop Route CT": {
				"doctype": "Shop CT",
			},
		},
		target_doc,
	)

	return target_doc