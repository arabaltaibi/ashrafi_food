import frappe

def execute(filters):
    columns, data = [], []

    # Define columns for the report
    columns = [
        {"label": "Supplier Name", "fieldname": "party", "fieldtype": "Link", "options": "Customer", "width": 150},
        {"label": "Mode of Payment", "fieldname": "mode_of_payment", "fieldtype": "Link", "options": "Mode of Payment", "width": 150},
        {"label": "Due Date", "fieldname": "cheque_date", "fieldtype": "Date", "width": 150},
        {"label": "Cheque Number", "fieldname": "cheque_number", "fieldtype": "Data", "width": 150},
        {"label": "Bank Name", "fieldname": "link_7", "fieldtype": "Link", "options": "Mode of Payment", "width": 150},
        {"label": "Amount", "fieldname": "amount_paid", "fieldtype": "Currency",  "width": 150},
    ]

    # Fetch filters
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    # Construct SQL query with date filters
    sql_query = """
        SELECT party, mode_of_payment, cheque_date, cheque_number, link_7, amount_paid
        FROM tabPDC
        WHERE docstatus=1
        AND payment_type="Pay"
    """
    if from_date:
        sql_query += f" AND posting_date >= '{from_date}'"
    if to_date:
        sql_query += f" AND posting_date <= '{to_date}'"

    # Fetch data based on filters
    data = frappe.db.sql(sql_query, as_dict=1)

    return columns, data
