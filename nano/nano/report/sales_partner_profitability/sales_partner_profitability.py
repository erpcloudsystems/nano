# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from frappe.utils import flt



def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters, columns)
    return columns, data

def get_columns():
    return [
        {
            "label": _("Sales Partner"),
            "fieldname": "sales_partner",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "label": _("Net Total"),
            "fieldname": "net_total",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("C.O.G.S"),
            "fieldname": "cogs",
            "fieldtype": "Currency",
            "width": 180
        },
        {
            "label": _("Gross Profit"),
            "fieldname": "gross_profit",
            "fieldtype": "Currency",
            "width": 180
        },
        {
            "label": _("Gross Profit %"),
            "fieldname": "gross_profit_percent",
            "fieldtype": "Percent",
            "width": 120
        },
        {
            "label": _("Outstanding"),
            "fieldname": "outstanding_amount",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Payable Commission"),
            "fieldname": "sales_partner_commission",
            "fieldtype": "Currency",
            "width": 160
        },
        {
            "label": _("Paid Commission"),
            "fieldname": "total_payable",
            "fieldtype": "Currency",
            "width": 140
        },
        {
            "label": _("Salary Slip"),
            "fieldname": "net_pay",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Net Profit"),
            "fieldname": "net_profit",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Net Profit %"),
            "fieldname": "net_profit_percent",
            "fieldtype": "Percent",
            "width": 120
        }
    ]

def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    if filters.get("sales_partner"):
        conditions += " and `tabSales Partner`.name=%(sales_partner)s"

    to_date = filters.get("to_date")
    from_date = filters.get("from_date")

    item_results = frappe.db.sql("""
        SELECT 
            `tabSales Partner`.name as sales_partner,
            
            IFNULL((select sum(net_total) 
            from `tabSales Invoice`
            where `tabSales Invoice`.docstatus = 1
            and `tabSales Invoice`.is_return = 0
            and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'
            and `tabSales Invoice`.sales_partner = `tabSales Partner`.name),0) as net_total,

            IFNULL((select sum(`tabSales Invoice Item`.qty * `tabSales Invoice Item`.incoming_rate) - sum(`tabSales Invoice Item`.amount)
            from `tabSales Invoice Item` join `tabSales Invoice` on `tabSales Invoice Item`.parent = `tabSales Invoice`.name
            where `tabSales Invoice`.docstatus = 1
            and `tabSales Invoice`.is_return = 0
            and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'
            and `tabSales Invoice`.sales_partner = `tabSales Partner`.name),0) as cogs,
            
            IFNULL((select sum(outstanding_amount) 
            from `tabSales Invoice`
            where `tabSales Invoice`.docstatus = 1
            and `tabSales Invoice`.is_return = 0
            and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'
            and `tabSales Invoice`.sales_partner = `tabSales Partner`.name),0) as outstanding_amount,
            
            IFNULL((select sum(sales_partner_commission) 
            from `tabSales Invoice`
            where `tabSales Invoice`.docstatus = 1
            and `tabSales Invoice`.is_return = 0
            and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'
            and `tabSales Invoice`.sales_partner = `tabSales Partner`.name),0) as sales_partner_commission,

            IFNULL((select sum(total_payable) 
            from `tabCommission Payment`
            where `tabCommission Payment`.docstatus = 1
            and `tabCommission Payment`.pay_to = "Sales Partner"
            and `tabCommission Payment`.posting_date between '{from_date}' and '{to_date}'
            and `tabCommission Payment`.sales_partner = `tabSales Partner`.name),0) as total_payable,
            
            IFNULL((select sum(net_pay) 
            from `tabSalary Slip`
            where `tabSalary Slip`.docstatus = 1
            and `tabSalary Slip`.posting_date between '{from_date}' and '{to_date}'
            and `tabSalary Slip`.employee = `tabSales Partner`.employee),0) as net_pay
            
        

        FROMa
            `tabSales Partner`
        WHERE
            `tabSales Partner`.disabled = 0
            {conditions}
        """.format(conditions=conditions, from_date=from_date, to_date=to_date), filters, as_dict=1)

    result = []
    if item_results:
        for item_dict in item_results:
            data = {
                'sales_partner': item_dict.sales_partner,
                #'gross_profit_percent': item_dict.gross_profit_percent,
                'gross_profit': item_dict.net_total + item_dict.cogs,
                'net_total': item_dict.net_total,
                'outstanding_amount': item_dict.outstanding_amount,
                'sales_partner_commission': item_dict.sales_partner_commission,
                'total_payable': item_dict.total_payable,
                'cogs': -1 * item_dict.cogs,
                'net_pay': item_dict.net_pay,
                'net_profit': (item_dict.net_total + item_dict.cogs) - (item_dict.sales_partner_commission + item_dict.net_pay),
            }

            result.append(data)


    return result
