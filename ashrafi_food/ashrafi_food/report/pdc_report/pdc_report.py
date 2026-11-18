import frappe

def execute(filters):
    columns, data = [], []

    # Define columns for the report
    columns = [
        {"label": "Customer Name", "fieldname": "party", "fieldtype": "Link", "options": "Customer", "width": 150},
        {"label": "Mode of Payment", "fieldname": "mode_of_payment", "fieldtype": "Link", "options": "Mode of Payment", "width": 150},
        {"label": "Due Date", "fieldname": "cheque_date", "fieldtype": "Date", "width": 150},
        {"label": "Cheque Number", "fieldname": "cheque_number", "fieldtype": "Data", "width": 150},
        {"label": "Bank Name", "fieldname": "link_7", "fieldtype": "Link", "options": "Bank", "width": 150},
        {"label": "Amount", "fieldname": "amount_paid", "fieldtype": "Currency",  "width": 150},
    ]

    # Fetch filters
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    # Construct SQL query with date and payment type filters
    receivable_query = """
        SELECT party, mode_of_payment, cheque_date, cheque_number, link_7, amount_paid
        FROM tabPDC
        WHERE docstatus = 1
        AND payment_type = 'Receive'
        AND clear= 0
    """
    payable_query = """
        SELECT party, mode_of_payment, cheque_date, cheque_number, link_7, amount_paid
        FROM tabPDC
        WHERE docstatus = 1
        AND payment_type = 'Pay'
        AND clear= 0
    """
    if from_date:
        receivable_query += f" AND posting_date >= '{from_date}'"
        payable_query += f" AND posting_date >= '{from_date}'"
    if to_date:
        receivable_query += f" AND posting_date <= '{to_date}'"
        payable_query += f" AND posting_date <= '{to_date}'"

    # Fetch receivable data based on filters
    receivable_data = frappe.db.sql(receivable_query, as_dict=1)

    # Fetch payable data based on filters
    payable_data = frappe.db.sql(payable_query, as_dict=1)

    receivable_total = sum(row['amount_paid'] for row in receivable_data)
    payable_total = sum(row['amount_paid'] for row in payable_data)
    data.append({
        "party": "RECEIVABLE ",
        "mode_of_payment": "",
        "cheque_date": "",
        "cheque_number": "",
        "link_7": "",
        "amount_paid": ""
    })
    # Append receivable data to rows
    for row in receivable_data:
        data.append(row)
    data.append({
        "party": "",
        "mode_of_payment": "",
        "cheque_date": "",
        "cheque_number": "",
        "link_7": "TOTAL",
        "amount_paid": receivable_total
    })
    data.append({
        "party": "PAYABLE",
        "mode_of_payment": "",
        "cheque_date": "",
        "cheque_number": "",
        "link_7": "",
        "amount_paid": ""
    })
    # Append payable data to rows
    for row in payable_data:
        data.append(row)
    data.append({
        "party": "",
        "mode_of_payment": "",
        "cheque_date": "",
        "cheque_number": "",
        "link_7": "TOTAL",
        "amount_paid": payable_total
    })
    data.append({
        "party": "",
        "mode_of_payment": "",
        "cheque_date": "",
        "cheque_number": "",
        "link_7": "BALANCE",
        "amount_paid": payable_total-receivable_total
    })
    # Append receivable total row
    

    # Append payable total row
    

    return columns, data
