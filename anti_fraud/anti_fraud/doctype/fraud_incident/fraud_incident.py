# Copyright (c) 2024, bti and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class FraudIncident(Document):
	def validate(self):
		self.validate_case_type()

	def validate_case_type(self):
		if self.case_fraud:
			type=frappe.db.get_value("Case Fraud",self.case_fraud,"the_relevant_department")
			if type != "Anti – Fraud Unit":
				frappe.throw("The relevant Department must be Anti – Fraud Unit")