// Copyright (c) 2021, ERP Cloud Systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Commission Payment',  'validate',  function(frm, cdt, cdn) {
    if(frm.doc.__islocal ? 0 : 1){
         var dw = locals[cdt][cdn];
        var total = 0;
        frm.doc.commission_details.forEach(function(dw) { total += dw.commissions; });
        frm.set_value("total_payable", total);
        refresh_field("total_payable");
    }
});

   frappe.ui.form.on("Commission Payment", {
    setup: function(frm) {
		frm.set_query("sales_manager", function() {
			return {
				filters: [
					["Sales Partner", "name", "in", ["Zainab Farouk","Khalid Matter"]]
				]
			};
		});
	}
});