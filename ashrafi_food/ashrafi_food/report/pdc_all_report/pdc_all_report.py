import frappe
from datetime import datetime, timedelta

def execute(filters):
    columns, data = [], []

    # Define columns
    columns = [
        {"label": "Invoice No.", "fieldname": "reference_name", "fieldtype": "Data", "width": 150},
        {"label": "Invoice Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 150},
        {"label": "Invoice Value", "fieldname": "total_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Cheque No", "fieldname": "cheque_number", "fieldtype": "Data", "width": 150},
        {"label": "Due Date", "fieldname": "cheque_date", "fieldtype": "Date", "width": 150},
        {"label": "Day Count", "fieldname": "due_date_plus_30", "fieldtype": "Date", "width": 150},
        {"label": "PDC Value", "fieldname": "amount_paid", "fieldtype": "Currency", "width": 150},
        # Add more columns as needed
    ]

    # Fetch data based on filters
    data = frappe.db.sql("""
        SELECT 
            per.reference_name,
            pdc.posting_date,
            per.total_amount,
            pdc.cheque_number,
            pdc.cheque_date,
            DATE_ADD(pdc.cheque_date, INTERVAL 30 DAY) AS due_date_plus_30,
            pdc.amount_paid
        FROM `tabPDC` AS pdc
            LEFT JOIN
        `tabPayment Entry Reference` AS per
            ON per.parent=pdc.name
        WHERE 
            pdc.docstatus = 1
            AND pdc.posting_date BETWEEN %(from_date)s AND %(to_date)s
            AND (pdc.party = %(party)s OR %(party)s IS NULL)
    """,{"from_date": filters.get("from_date"), "to_date": filters.get("to_date"), "party": filters.get("party")}, as_dict=1)

    return columns, data
