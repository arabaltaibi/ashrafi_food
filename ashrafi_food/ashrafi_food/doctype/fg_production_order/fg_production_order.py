# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class FGProductionOrder(Document):
	@frappe.whitelist()
	def get_items(self):
		self.items = []
		fg = frappe.get_doc('Finished Good Template', self.finished_good)
		for row in fg.items:
			it = self.append('items')
			it.item_code = row.item_code
			it.qty = (row.qty * self.qty)/fg.qty
			it.source_warehouse = row.source_warehouse
		#self.save()
	def before_submit(self):
		self.create_se()

	def on_cancel(self):
		self.cancel_fg_se()

	@frappe.whitelist()
	def cancel_fg_se(self):
		if self.linked_se:
			doc = frappe.get_doc('Stock Entry', self.linked_se)
			doc.cancel()
			doc.delete()
	def create_se(self):
		se = frappe.new_doc('Stock Entry')
		se.company = self.company
		se.stock_entry_type = 'Manufacture'
		se.set_posting_time = 1
		se.posting_date = self.date
		se.posting_time = self.posting_time

		for item in self.items:
			if item.is_scrap_item == 0:
				sei = se.append('items')
				sei.item_code = item.item_code
				sei.qty = item.qty
				sei.s_warehouse = item.source_warehouse
				sei.cost_center = self.cost_center
			if item.is_scrap_item ==1:
				scrap = se.append('items')
				scrap.item_code = item.item_code
				scrap.t_warehouse = item.scrap_warehouse
				scrap.qty = item.qty
				scrap.is_scrap_item = item.is_scrap_item
				scrap.cost_center = self.cost_center
		se.append('items', {'item_code': self.item_code, 'qty':self.qty, 't_warehouse': self.target_warehouse, 'cost_center': self.cost_center, 'is_finished_item': 1})
		se.save()
		self.linked_se = se.name
		se.submit()