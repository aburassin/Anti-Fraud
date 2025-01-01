# Copyright (c) 2024, bti and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class InvestigationActionSetting(Document):
	
	def validate(self):
		
		# self.check_percentage_is_correct()
		self.check_percentage_in_score()


	def check_percentage_is_correct(self):
		self_dict=self.as_dict()
		tables=["instant_action","later_action"]
		for table in tables:
			total=0
			for idx in self_dict[table]:
				total+=idx["weight"]
			if total != 100:
				frappe.throw("Total weight in {0} must equal 100%".format(table))

	def check_percentage_in_score(self):
		self_dict=self.as_dict()
		tables=["instant_action_score","later_action_score"]
		for table in tables:
			percent=None

			for idx in self_dict[table]:
				if idx["weight"] == 100:
					percent=100
			if not percent:
				frappe.throw("At least on of row must equal 100% in {0}".format(table))