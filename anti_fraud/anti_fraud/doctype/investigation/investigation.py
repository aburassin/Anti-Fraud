# Copyright (c) 2024, bti and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Investigation(Document):
    pass

    @frappe.whitelist()
    def create_investigation_action(self,action_type):
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