# Copyright (c) 2024, bti and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class FraudInvestigation(Document):
    def before_submit(self):
        self.check_action_created()


    
    def check_action_created(self):
        investigation=frappe.db.exists("Investigation Action", {"investigation": self.name,"docstatus":1})
        if not investigation:
            frappe.throw("Please create <b style='color:red'>Submittable Action</b>")

    @frappe.whitelist()
    def create_investigation_report(self):
        investigation_action=frappe.db.exists("Investigation Action", {"investigation": self.name,"docstatus":1})
       
        if not investigation_action:
            frappe.throw("Please create <b style='color:red'>Submittable Action</b>")

        fraud_incident= frappe.get_doc("Fraud Incident",self.fraud_incident)

        investigation_report=frappe.new_doc("Investigation Report")
        investigation_report.fraud_investigation=self.name
        investigation_report.case_fraud=self.case_fraud
        investigation_report.fraud_incident=self.fraud_incident
        investigation_report.investigation_action=investigation_action

        for i in fraud_incident.document:
            investigation_report.append("documents",{
                "document_type":i.document_type,
                "document":i.document,
                "submission_date":i.submission_date,
                "verification_status":i.verification_status,
                "verified_by":i.verified_by,
                "remarks":i.verified_by,
            })

        investigation_report.flags.ignore_permissions = 1
        investigation_report.flags.ignore_mandatory = True
        investigation_report.insert()

        Url = frappe.utils.get_url_to_form(investigation_report.doctype, investigation_report.name)
        # show message after succues with hyperlink
        frappe.msgprint('Investigation Report Created Successfully  <a href={0} > {1} </a>'.format(Url, investigation_report.name))

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
        action.investigation=self.name
        action.case_fraud=self.case_fraud
        action.financial_fraud_method=self.financial_fraud_method
        action.fraud_incident=self.fraud_incident
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