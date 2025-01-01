# Copyright (c) 2024, bti and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class InvestigationAction(Document):
    
    def validate(self):
        self.get_score()

    def get_score(self):
        if self.financial_fraud_method=="العميل يقدم مستندات مزورة":
            info={"Instant Action":"forgery_instant_action","Later Action":"forgery_later_action"}
        else:
            info={"Instant Action":"instant_action","Later Action":"later_action"}
        setting=frappe.get_doc("Investigation Action Setting").as_dict()
        
        if len(self.action):
            weight=0
            for i in self.action:
                weight+=self.get_setting_weight(setting,self.type,i.question,info,i.answer)
            
            self.scoring=str(weight)
            self.potential_fraud=self.get_class(setting,self.scoring,self.type)
            
            
    def get_setting_weight(self,setting,type,question,info,answer):
       
        for i in setting[info[type]]:
            
            if question == i["question"] and answer==i["condition"]:
                  
                    return int(i["weight"])
            
        return 0
    
    def get_class(self, setting, point,type):
        if self.financial_fraud_method=="العميل يقدم مستندات مزورة":
            info={"Instant Action":"forgery_instant_action_score","Later Action":"forgery_later_action_score"}
        else:
            info={"Instant Action":"instant_action_score","Later Action":"later_action_score"}
        sorted_classes = sorted(
            setting[info[type]], key=lambda x: x["weight"], reverse=False
        )

        result = None

        for row in setting[info[type]]:
            if int(point) >= row["weight"]:
                result = row["potential_fraud"]

        return result