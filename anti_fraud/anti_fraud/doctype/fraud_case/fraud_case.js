// Copyright (c) 2024, bti and contributors
// For license information, please see license.txt

frappe.ui.form.on("Fraud Case", {
  refresh: function (frm) {
    frm.events.set_fraud_incident_btn(frm);
    frm.events.set_cs_team_btn(frm);
    // TODO: to be remove
    frm.events.migrate_date(frm);
  },
  migrate_date: function (frm) {
    frm.add_custom_button("Migrate Data", () => {
      frm.call({
        method: "migrate_data",
        doc: frm.doc,
        callback: function (r) {},
      });
    });
  },
  set_fraud_incident_btn: function (frm) {
    frappe.db

      .get_value("Fraud Incident", { case_fraud: frm.doc.name }, "name")
      .then((r) => {
        if (!r.message.name) {
          if (
            !frm.is_new() &&
            frm.doc.docstatus == 1 &&
            frm.doc.the_relevant_department == "Anti – Fraud Unit"
          ) {
            frm.add_custom_button("Create Fraud Incident", () => {
              frappe.new_doc("Fraud Incident", {
                case_fraud: cur_frm.doc.name,
                customer: cur_frm.doc.customer,
                customer_name: cur_frm.doc.customer_name,
                customer_phone_number: cur_frm.doc.customer_phone_number,
                loss_amount: cur_frm.doc.loss_amount,
              });
            });
          }
        }
      });
  },
  is_a_fraud_case_opened: function (frm) {
    if (frm.doc.is_a_fraud_case_opened == "Yes") {
      frm.set_value("the_relevant_department", "Anti – Fraud Unit");
    } else {
      frm.set_value("the_relevant_department", "CS team");
    }
  },
  set_cs_team_btn: function (frm) {
    if (
      !frm.is_new() &&
      frm.doc.docstatus == 1 &&
      frm.doc.the_relevant_department == "CS team"
    ) {
      frm.add_custom_button("Sent To CS team", () => {
        frappe.show_alert(
          {
            message: __("Hi, This service is under development."),
            indicator: "red",
          },
          5
        );
      });
    }
  },
});
