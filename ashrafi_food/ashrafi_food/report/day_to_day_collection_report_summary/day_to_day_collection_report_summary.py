import frappe

def execute(filters):
    columns, data = [], []

    # Define columns
    columns = [
        {"label": "Sales Person", "fieldname": "user_name", "fieldtype": "Data", "width": 150},
       # {"label": "Sales Person2", "fieldname": "user_name", "fieldtype": "Data", "width": 150},
        {"label": "Cash", "fieldname": "cash_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Wire Transfer", "fieldname": "wire_transfer_amount", "fieldtype": "Currency", "width": 200},
        {"label": "PDC", "fieldname": "amount_paid", "fieldtype": "Currency", "width": 200}
        # Add more columns as needed
    ]

    # Fetch data based on filters
    data = frappe.db.sql("""
        SELECT pe.user_name,
               SUM(CASE WHEN pe.mode_of_payment = 'Cash' THEN pe.paid_amount ELSE 0 END) AS cash_amount,
               SUM(CASE WHEN pe.mode_of_payment = 'Wire Transfer' THEN pe.paid_amount ELSE 0 END) AS wire_transfer_amount,
               SUM(pdc.amount_paid) AS amount_paid
        FROM `tabPayment Entry` AS pe
        RIGHT JOIN `tabPDC` AS pdc
        ON pdc.user_name=pe.user_name
        #GROUP BY pe.user_name
        HAVING cash_amount != 0 OR wire_transfer_amount != 0 OR amount_paid != 0
    """, as_dict=1)

    return columns, data
