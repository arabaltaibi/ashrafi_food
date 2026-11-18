import frappe

def execute(filters):
    columns, data = [], []

    # Define columns for the report
    columns = [
        {"label": "Sales Person", "fieldname": "user_name", "fieldtype": "Data", "width": 150},
        {"label": "Customer", "fieldname": "party", "fieldtype": "Link", "options": "Customer", "width": 150},
        {"label": "Cash", "fieldname": "paid_amount", "fieldtype": "Currency", "width": 150}
        
    ]

    # Fetch filters
    # from_date = filters.get("from_date")
    # to_date = filters.get("to_date")

    # Construct SQL query with date and payment type filters
    cash_query = """
        SELECT user_name, party, paid_amount
        FROM `tabPayment Entry`
        Where mode_of_payment="Cash"
        AND party_type="Customer"
        AND docstatus = 1
        
    """
    wire_query = """
        SELECT user_name, party, paid_amount
        FROM `tabPayment Entry`
        WHERE docstatus = 1
        AND party_type="Customer"
        AND mode_of_payment="Wire Transfer"
    """
    # if from_date:
    #     receivable_query += f" AND posting_date >= '{from_date}'"
    #     payable_query += f" AND posting_date >= '{from_date}'"
    # if to_date:
    #     receivable_query += f" AND posting_date <= '{to_date}'"
    #     payable_query += f" AND posting_date <= '{to_date}'"

    
    cash_data = frappe.db.sql(cash_query, as_dict=1)

    
    wire_data = frappe.db.sql(wire_query, as_dict=1)

    cash_total = sum(row['paid_amount'] for row in cash_data)
    wire_total = sum(row['paid_amount'] for row in wire_data)
    for row in cash_data:
        data.append(row)
    data.append({
        "user_name": "",
        "party": "TOTAL",
        "paid_amount": cash_total
    })
    data.append({
        "user_name": "Sales Person",
        "party": "Customer",
        "paid_amount": "Wire Transfer"
    })
    
    for row in wire_data:
        data.append(row)
    data.append({
        "user_name": "",
        "party": "TOTAL",
        "paid_amount": wire_total
    })
    
   
    

    return columns, data
