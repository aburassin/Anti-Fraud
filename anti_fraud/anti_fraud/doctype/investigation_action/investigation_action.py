# Copyright (c) 2024, bti and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class InvestigationAction(Document):
    
    def validate(self):
        self.get_score()

    def get_score(self):
        info={"Instant Action":"instant_action","Later Action":"later_action"}
        setting=frappe.get_doc("Investigation Action Setting").as_dict()
        
        if len(self.action):
            weight=0
            for i in self.action:
                if i.answer =="Yes":
                    weight+=self.get_setting_weight(setting,self.type,i.question,info)

            self.scoring=str(weight)
            self.potential_fraud=self.get_class(setting,self.scoring,self.type)
    def get_setting_weight(self,setting,type,question,info):
       
        for i in setting[info[type]]:
            
            if question == i["question"]:
                    return int(i["weight"])
    
    def get_class(self, setting, point,type):
        info={"Instant Action":"instant_action_score","Later Action":"later_action_score"}
        sorted_classes = sorted(
            setting[info[type]], key=lambda x: x["weight"], reverse=False
        )

        result = None

        for row in setting[info[type]]:
            if int(point) >= row["weight"]:
                result = row["potential_fraud"]

        return result