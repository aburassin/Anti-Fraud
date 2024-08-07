// Copyright (c) 2024, bti and contributors
// For license information, please see license.txt

frappe.ui.form.on("Fraud Investigation", {
  refresh: function (frm) {
    frappe.db
      .get_value(
        "Investigation Action",
        { investigation: frm.doc.name },
        "name"
      )
      .then((r) => {
        if (!r.message.name) {
          frm.events.set_action_btn(frm);
        }
      });
    frappe.db
      .get_value(
        "Investigation Report",
        { fraud_investigation: frm.doc.name },
        "name"
      )
      .then((r) => {
        if (!r.message.name) {
          frm.events.set_investigation_report_btn(frm);
        }
      });
  },
  set_investigation_report_btn: function (frm) {
    if (frm.doc.docstatus == 1) {
      frm.add_custom_button("Create Investigation Report", () => {
        frappe.call({
          doc: frm.doc,
          method: "create_investigation_report",
          callback: (r) => {
            cur_frm.reload_doc();
          },
        });
      });
    }
  },
  set_action_btn: function (frm) {
    if (!frm.is_new() || frm.doc.docstatus == 0) {
      frm.add_custom_button(
        "Later",
        () => {
          frappe.call({
            doc: frm.doc,
            args: { action_type: "Later Action" },
            method: "create_investigation_action",
            callback: (r) => {
              cur_frm.reload();
            },
          });
        },
        "Take Action"
      );
    }
  },
});
