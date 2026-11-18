import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("AREA NAME"), "fieldname": "area_name", "fieldtype": "Link", "options": "Warehouse", "width": 150},
        # LOAD OUT Section
        {"label": _("F-10"), "fieldname": "load_f10", "fieldtype": "Float", "width": 70},
        {"label": _("F-05"), "fieldname": "load_f05", "fieldtype": "Float", "width": 70},
        {"label": _("FINE"), "fieldname": "load_fine", "fieldtype": "Float", "width": 70},
        {"label": _("C-10"), "fieldname": "load_c10", "fieldtype": "Float", "width": 70},
        {"label": _("C-05"), "fieldname": "load_c05", "fieldtype": "Float", "width": 70},
        {"label": _("CHAKKI"), "fieldname": "load_chakki", "fieldtype": "Float", "width": 70},
        {"label": _("FL-10"), "fieldname": "load_fl10", "fieldtype": "Float", "width": 70},
        {"label": _("FL-05"), "fieldname": "load_fl05", "fieldtype": "Float", "width": 70},
        {"label": _("FLUORIO"), "fieldname": "load_fluorio", "fieldtype": "Float", "width": 70},
        {"label": _("TOTAL"), "fieldname": "load_total", "fieldtype": "Float", "width": 80},
        # SALE Section
        {"label": _("F-10"), "fieldname": "sale_f10", "fieldtype": "Float", "width": 70},
        {"label": _("F-05"), "fieldname": "sale_f05", "fieldtype": "Float", "width": 70},
        {"label": _("FINE"), "fieldname": "sale_fine", "fieldtype": "Float", "width": 70},
        {"label": _("C-10"), "fieldname": "sale_c10", "fieldtype": "Float", "width": 70},
        {"label": _("C-05"), "fieldname": "sale_c05", "fieldtype": "Float", "width": 70},
        {"label": _("CHAKKI"), "fieldname": "sale_chakki", "fieldtype": "Float", "width": 70},
        {"label": _("FL-10"), "fieldname": "sale_fl10", "fieldtype": "Float", "width": 70},
        {"label": _("FL-05"), "fieldname": "sale_fl05", "fieldtype": "Float", "width": 70},
        {"label": _("FLUORIO"), "fieldname": "sale_fluorio", "fieldtype": "Float", "width": 70},
        {"label": _("TOTAL"), "fieldname": "sale_total", "fieldtype": "Float", "width": 80},
        # BALANCE Section
        {"label": _("FRESH"), "fieldname": "balance_fresh", "fieldtype": "Float", "width": 80},
        {"label": _("DAMAGE"), "fieldname": "balance_damage", "fieldtype": "Float", "width": 80},

        {"label": _("LOAD OUT"), "fieldname": "load_out", "fieldtype": "Float", "width": 80}
    ]

def get_data(filters):
    warehouses = frappe.get_all("Warehouse", filters={"is_group": 0}, pluck="name")
    data = []
    
    for warehouse in warehouses:
        row = {
            "area_name": warehouse,
            **{field: 0 for field in [
                "load_f10", "load_f05", "load_fine", 
                "load_c10", "load_c05", "load_chakki", 
                "load_fl10", "load_fl05", "load_fluorio", "load_total",
                "sale_f10", "sale_f05", "sale_fine", 
                "sale_c10", "sale_c05", "sale_chakki", 
                "sale_fl10", "sale_fl05", "sale_fluorio", "sale_total",
                "balance_fresh", "balance_damage"
            ]}
        }
        
        # 1. LOAD OUT DATA
        load_data = frappe.db.sql("""
            SELECT item_code, SUM(qty) as qty
            FROM `tabStock Entry Detail`
            WHERE parent IN (
                SELECT name FROM `tabStock Entry`
                WHERE stock_entry_type = 'Material Loading'
                AND posting_date BETWEEN %(from_date)s AND %(to_date)s
                AND docstatus = 1
            )
            AND item_code IN ('F-10', 'F-05', 'C-10', 'C-05', 'FL-10', 'FL-05')
            AND t_warehouse = %(warehouse)s
            GROUP BY item_code
        """, {"warehouse": warehouse, **filters}, as_dict=1)
        
        for d in load_data:
            if d.item_code == "F-10": row["load_f10"] = d.qty
            if d.item_code == "F-05": row["load_f05"] = d.qty
            if d.item_code == "C-10": row["load_c10"] = d.qty
            if d.item_code == "C-05": row["load_c05"] = d.qty
            if d.item_code == "FL-10": row["load_fl10"] = d.qty
            if d.item_code == "FL-05": row["load_fl05"] = d.qty
        
        # Calculate computed columns
        row["load_fine"] = row["load_f10"] + (row["load_f05"] / 2)
        row["load_chakki"] = row["load_c10"] + (row["load_c05"] / 2)
        row["load_fluorio"] = row["load_fl10"] + (row["load_fl05"] / 2)
        row["load_total"] = row["load_fine"] + row["load_chakki"] + row["load_fluorio"]
        
        # 2. SALE DATA
        sale_data = frappe.db.sql("""
            SELECT item_code, SUM(qty) as qty
            FROM `tabSales Invoice Item`
            WHERE parent IN (
                SELECT name FROM `tabSales Invoice`
                WHERE posting_date BETWEEN %(from_date)s AND %(to_date)s
                AND docstatus = 1
            )
            AND item_code IN ('F-10', 'F-05', 'C-10', 'C-05', 'FL-10', 'FL-05')
            AND warehouse = %(warehouse)s
            GROUP BY item_code
        """, {"warehouse": warehouse, **filters}, as_dict=1)
        
        for d in sale_data:
            if d.item_code == "F-10": row["sale_f10"] = d.qty
            if d.item_code == "F-05": row["sale_f05"] = d.qty
            if d.item_code == "C-10": row["sale_c10"] = d.qty
            if d.item_code == "C-05": row["sale_c05"] = d.qty
            if d.item_code == "FL-10": row["sale_fl10"] = d.qty
            if d.item_code == "FL-05": row["sale_fl05"] = d.qty
        
        # Calculate computed columns
        row["sale_fine"] = row["sale_f10"] + (row["sale_f05"] / 2)
        row["sale_chakki"] = row["sale_c10"] + (row["sale_c05"] / 2)
        row["sale_fluorio"] = row["sale_fl10"] + (row["sale_fl05"] / 2)
        row["sale_total"] = row["sale_fine"] + row["sale_chakki"] + row["sale_fluorio"]
        
        # 3. BALANCE DATA
        balance_data = frappe.db.sql("""
            SELECT 
                SUM(IF(t_warehouse LIKE '%%Fresh%%', qty, 0)) as fresh,
                SUM(IF(t_warehouse LIKE '%%Damaged%%', qty, 0)) as damage
            FROM `tabStock Entry Detail`
            WHERE parent IN (
                SELECT name FROM `tabStock Entry`
                WHERE stock_entry_type = 'Material Unloading'
                AND posting_date BETWEEN %(from_date)s AND %(to_date)s
                AND docstatus = 1
            )
            AND s_warehouse = %(warehouse)s
        """, {"warehouse": warehouse, **filters}, as_dict=1)
        
        if balance_data and balance_data[0]:
            row["balance_fresh"] = balance_data[0].get("fresh", 0) or 0
            row["balance_damage"] = balance_data[0].get("damage", 0) or 0
        
        # Skip row if all numeric values are zero
        numeric_fields = [
            "load_f10", "load_f05", "load_fine", "load_c10", "load_c05", "load_chakki", 
            "load_fl10", "load_fl05", "load_fluorio", "load_total",
            "sale_f10", "sale_f05", "sale_fine", "sale_c10", "sale_c05", "sale_chakki", 
            "sale_fl10", "sale_fl05", "sale_fluorio", "sale_total",
            "balance_fresh", "balance_damage"
        ]
        
        row["load_out"] = row["sale_total"] + row["balance_damage"] + row["balance_fresh"]
        if not any(row[field] for field in numeric_fields):
            continue  # Skip this row
        
        data.append(row)
    
    # Add totals row if there's data
    if data:
        total_row = {"area_name": "TOTAL"}
        for key in data[0].keys():
            if key != "area_name":
                total_row[key] = sum(d.get(key, 0) for d in data)
        data.append(total_row)
    
    return data

