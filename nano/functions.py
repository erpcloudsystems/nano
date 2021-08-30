from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import cint, cstr, date_diff, flt, formatdate, getdate, get_link_to_form, get_fullname, add_days, nowdate, get_datetime
from erpnext.hr.utils import set_employee_name, get_leave_period, share_doc_with_approver
from erpnext.hr.doctype.leave_block_list.leave_block_list import get_applicable_block_dates
from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee
from erpnext.buying.doctype.supplier_scorecard.supplier_scorecard import daterange
from erpnext.hr.doctype.leave_ledger_entry.leave_ledger_entry import create_leave_ledger_entry
from frappe.model.document import Document

from datetime import timedelta, datetime

@frappe.whitelist()
def commission_cal():
    for_partner = frappe.db.sql(""" update `tabSales Invoice` set sales_partner_commission = (select(ifnull(sum(`tabSales Invoice Item`.net_amount), 0)*`tabSales Invoice`.commission_rate / 100) from `tabSalesInvoice Item`  where `tabSales Invoice Item`.parent = `tabSales Invoice`.name and `tabSales Invoice Item `.item_group != 'Services' """)
    for_manager = frappe.db.sql(""" update `tabSales Invoice` set sales_manager_commission = (select(ifnull(sum(`tabSales Invoice Item`.net_amount), 0)*`tabSales Invoice`.commission_rate / 100/4) from `tabSalesInvoice Item`  where `tabSales Invoice Item`.parent = `tabSales Invoice`.name and `tabSales Invoice Item `.item_group != 'Services' and `tabSales Invoice Item `.item_group != 'Rain Bird' and `tabSales Invoice Item `.item_group != 'Rain Bird Landscape' """)
    return for_manager, for_partner