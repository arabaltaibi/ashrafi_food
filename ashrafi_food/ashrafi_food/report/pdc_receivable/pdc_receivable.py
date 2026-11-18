import frappe

def execute(filters):
    columns, data = [], []

    
    columns = [
        {"label": "Customer Name", "fieldname": "party", "fieldtype": "Link", "options": "Customer", "width": 150},
        {"label": "Mode of Payment", "fieldname": "mode_of_payment", "fieldtype": "Link", "options": "Mode of Payment", "width": 150},
        {"label": "Due Date", "fieldname": "cheque_date", "fieldtype": "Date", "width": 150},
        {"label": "Cheque Number", "fieldname": "cheque_number", "fieldtype": "Data", "width": 150},
        {"label": "Bank Name", "fieldname": "link_7", "fieldtype": "Link", "options": "Mode of Payment", "width": 150},
        {"label": "Amount", "fieldname": "amount_paid", "fieldtype": "Currency",  "width": 150},
    ]

    
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    
    sql_query = """
        SELECT party, mode_of_payment, cheque_date, cheque_number, link_7, amount_paid
        FROM tabPDC
        WHERE docstatus = 1
	AND payment_type="Receive"
    """
    if from_date:
        sql_query += f" AND cheque_date >= '{from_date}'"
    if to_date:
        sql_query += f" AND cheque_date <= '{to_date}'"

    
    data = frappe.db.sql(sql_query, as_dict=1)

    return columns, data
