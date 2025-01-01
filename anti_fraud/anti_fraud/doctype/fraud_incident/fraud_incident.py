# Copyright (c) 2024, bti and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class FraudIncident(Document):
    def validate(self):
        self.validate_case_type()

    def validate_case_type(self):
        if self.case_fraud:
            type=frappe.db.get_value("Fraud Case",self.case_fraud,"the_relevant_department")
            if type != "Anti – Fraud Unit":
                frappe.throw("The relevant Department must be Anti – Fraud Unit")

    @frappe.whitelist()
    def create_investigation(self):
        doc=frappe.new_doc("Fraud Investigation")
        doc.case_fraud=self.case_fraud,
        doc.fraud_incident=self.name,
        doc.financial_fraud_method=self.financial_fraud_method
        if len(self.document):
            for i in self.document:
                doc.append("document",{
                    "document_type":i.document_type,
                    "document":i.document
                })
        doc.insert()
        Url = frappe.utils.get_url_to_form(doc.doctype, doc.name)
        # show message after succues with hyperlink
        frappe.msgprint('Investigation  Created Successfully  <a href={0} > {1} </a>'.format(Url, doc.name))        
    @frappe.whitelist()
    def create_investigation_action(self,action_type):
        if self.financial_fraud_method=="العميل يقدم مستندات مزورة":
            info={"Instant Action":"forgery_instant_action","Later Action":"forgery_later_action"}
        else:
            info={"Instant Action":"instant_action","Later Action":"later_action"}
        setting=frappe.get_doc("Investigation Action Setting").as_dict()

        self.validate_action_question(setting,action_type,info)
        action=frappe.new_doc("Investigation Action")
        for i in setting[info[action_type]]:
            action.append("action",{
                "question":i["question"]
            })
        action.type=action_type
 
        action.case_fraud=self.case_fraud
        action.financial_fraud_method=self.financial_fraud_method
        action.fraud_incident=self.name
        action.flags.ignore_permissions = 1
        action.flags.ignore_mandatory = True
        action.insert()
        Url = frappe.utils.get_url_to_form(action.doctype, action.name)
        # show message after succues with hyperlink
        frappe.msgprint('Investigation Action Created Successfully  <a href={0} > {1} </a>'.format(Url, action.name))

    def validate_action_question(self,setting,action_type,info):
        
        if not len(setting[info[action_type]]):
            Url = frappe.utils.get_url_to_form("Investigation Action Setting", "Investigation Action Setting",)
            frappe.throw("Please set {0} List in  <a href={1} > <b>Setting</b> </a>".format(action_type,Url))