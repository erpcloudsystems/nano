// Copyright (c) 2016, ERP Cloud Systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Partner Profitability"] = {
	"filters": [
		{
			fieldname: "sales_partner",
			label: __("Sales Partner"),
			fieldtype: "Link",
			options: "Sales Partner"
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			fieldname:"to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today()
		},
	]
}
