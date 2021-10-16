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
    frappe.db.sql(""" update `tabSales Invoice` join `tabSales Partner` on `tabSales Invoice`.sales_partner = `tabSales Partner`.name set `tabSales Invoice`.commission_rate  = `tabSales Partner`.commission_rate """)
    frappe.db.sql(""" update `tabSales Invoice Item` join `tabItem` on `tabSales Invoice Item`.item_code = `tabItem`.name set `tabSales Invoice Item`.item_group  = `tabItem`.item_group """)
    frappe.db.sql(""" update `tabSales Invoice Item` join `tabSales Invoice` on `tabSales Invoice Item`.parent = `tabSales Invoice`.name set `tabSales Invoice Item`.net_commission = (ifnull(`tabSales Invoice Item`.net_amount,0) * `tabSales Invoice`.commission_rate / 100) where `tabSales Invoice Item`.item_group != 'Services' """)
    frappe.db.sql(""" update `tabSales Invoice Item` join `tabSales Invoice` on `tabSales Invoice Item`.parent = `tabSales Invoice`.name set `tabSales Invoice Item`.net_manager_commission = (ifnull(`tabSales Invoice Item`.net_amount,0) * `tabSales Invoice`.commission_rate / 100/4) where `tabSales Invoice Item`.item_group != 'Services' and `tabSales Invoice Item`.item_group != 'Rain Bird' and `tabSales Invoice Item`.item_group != 'Rain Bird Landscape' """)
    frappe.db.sql(""" update `tabSales Invoice` set sales_partner_commission = (select(ifnull(sum(`tabSales Invoice Item`.net_amount), 0)*`tabSales Invoice`.commission_rate / 100) from `tabSales Invoice Item`  where `tabSales Invoice Item`.parent = `tabSales Invoice`.name and `tabSales Invoice Item`.item_group != 'Services') """)
    frappe.db.sql(""" update `tabSales Invoice` set sales_manager_commission = (select(ifnull(sum(`tabSales Invoice Item`.net_amount), 0)*`tabSales Invoice`.commission_rate / 100/4) from `tabSales Invoice Item`  where `tabSales Invoice Item`.parent = `tabSales Invoice`.name and `tabSales Invoice Item`.item_group != 'Services' and `tabSales Invoice Item`.item_group != 'Rain Bird' and `tabSales Invoice Item`.item_group != 'Rain Bird Landscape') """)
    #return Commisions, item_group, for_partner_item, for_manager_item, for_partner, for_manager