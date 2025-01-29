# Copyright (c) 2024, bti and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
class FraudCase(Document):
    
    @frappe.whitelist()
    def migrate_data(self):
        cases=frappe.db.get_all("Fraud Case",filters={"docstatus":1},pluck="name")
        if len(cases):
                for case in cases:
                    incident= frappe.db.exists("Fraud Incident", {"case_fraud": case})
                    if incident:
                        customer,customer_name,customer_phone_number,loss_amount=frappe.db.get_value("Fraud Case",case,["customer","customer_name","customer_phone_number","loss_amount"])
                        frappe.db.set_value("Fraud Incident",incident,"customer",customer)
                        frappe.db.set_value("Fraud Incident",incident,"customer_name",customer_name)
                        frappe.db.set_value("Fraud Incident",incident,"customer_phone_number",customer_phone_number)
                        frappe.db.set_value("Fraud Incident",incident,"loss_amount",loss_amount)
                        
        incidents = frappe.db.get_all("Fraud Incident", filters={"docstatus": 1}, pluck="name")

        if incidents:
                for incident in incidents:
                    incident_doc = frappe.get_doc("Fraud Incident", incident)

                    if incident_doc.suspect:
                        investigation = frappe.db.exists("Fraud Investigation", {"fraud_incident": incident})

                        if investigation:
                           
                            investigation_doc = frappe.get_doc("Fraud Investigation", investigation)
                            if not len(investigation_doc.suspect):
                                for i in incident_doc.suspect:
                                    child_name = make_autoname("FIS-.#####")
                                    frappe.db.sql("""
                                                INSERT INTO `tabFraud Incident Suspect` 
                                                (`name`, `parent`, `parentfield`, `parenttype`, `suspect_name`, `phone_number`, `civil_id`, `nationality`, `fraud_list`, `idx`, `docstatus`)
                                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                            """, (
                                                child_name, 
                                                investigation_doc.name,  
                                                "suspect",  
                                                "Fraud Investigation",  
                                                i.suspect_name,
                                                i.phone_number,
                                                i.civil_id,
                                                i.nationality,
                                                i.fraud_list,
                                                len(investigation_doc.suspect) + 1, 
                                                1  
                                            ))

                            frappe.db.commit()

                                
        
        
        frappe.msgprint("Data Migrated Successfully")