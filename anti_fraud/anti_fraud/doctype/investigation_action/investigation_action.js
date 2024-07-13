// Copyright (c) 2024, bti and contributors
// For license information, please see license.txt

frappe.ui.form.on("Investigation Action", {
  onload: function (frm) {
    frm.get_field("action").grid.cannot_add_rows = true;
  },
  refresh: function (frm) {
    frm.get_field("action").grid.cannot_add_rows = true;
  },
});
