// Copyright (c) 2024, bti and contributors
// For license information, please see license.txt

frappe.ui.form.on("Fraud Incident", {
  refresh: function (frm) {
    frm.events.set_investigation_btn(frm);
  },
  set_investigation_btn: function (frm) {
    if (!frm.is_new() && frm.doc.docstatus == 1) {
      frm.add_custom_button("Create Investigation", () => {
        frappe.new_doc("Investigation", {
          case_fraud: cur_frm.doc.case_fraud,
          fraud_incident: cur_frm.doc.name,
        });
      });
    }
  },
});
