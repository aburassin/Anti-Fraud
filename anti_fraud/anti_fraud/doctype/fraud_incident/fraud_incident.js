// Copyright (c) 2024, bti and contributors
// For license information, please see license.txt

frappe.ui.form.on("Fraud Incident", {
  refresh: function (frm) {
    if (!frm.is_new() && frm.doc.docstatus == 1) {
      frappe.db

        .get_value(
          "Investigation Action",
          { fraud_incident: frm.doc.name },
          "name"
        )
        .then((r) => {
          if (!r.message.name) {
            frm.events.set_action_btn(frm);
          } else {
            frm.events.set_investigation_btn(frm);
          }
        });
    }
  },
  set_investigation_btn: function (frm) {
    if (!frm.is_new() && frm.doc.docstatus == 1) {
      frm.add_custom_button("Create Fraud Investigation", () => {
        frappe.new_doc("Fraud Investigation", {
          case_fraud: cur_frm.doc.case_fraud,
          fraud_incident: cur_frm.doc.name,
        });
      });
    }
  },
  set_action_btn: function (frm) {
    frm.add_custom_button(
      "Instanse",
      () => {
        frappe.call({
          doc: frm.doc,
          args: { action_type: "Instant Action" },
          method: "create_investigation_action",
          callback: (r) => {
            cur_frm.reload_doc();
          },
        });
      },
      "Take Action"
    );
  },
});
