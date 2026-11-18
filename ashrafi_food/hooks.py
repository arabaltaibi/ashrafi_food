from . import __version__ as app_version

app_name = "ashrafi_food"
app_title = "Ashrafi Food"
app_publisher = "VFG"
app_description = "Ashrafi Foods"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "shahrukh@ventureforceglobal.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ashrafi_food/css/ashrafi_food.css"
# app_include_js = "/assets/ashrafi_food/js/ashrafi_food.js"

# include js, css files in header of web template
# web_include_css = "/assets/ashrafi_food/css/ashrafi_food.css"
# web_include_js = "/assets/ashrafi_food/js/ashrafi_food.js"

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_list_js = {
	"Delivery Note": "public/js/delivery_note_list.js",
	"Purchase Receipt": "public/js/purchase_receipt_list.js",
}

# Installation
# ------------

# before_install = "ashrafi_food.install.before_install"
# after_install = "ashrafi_food.install.after_install"

# DocType Class
# ---------------
# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# doc_events = {
#	"*": {
#		"on_update": "method",
#	}
# }

# Scheduled Tasks
# ---------------
# scheduler_events = {
#	"daily": [
#		"ashrafi_food.tasks.daily"
#	],
# }

# Overriding Methods
# ------------------------------
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "ashrafi_food.event.get_events"
# }


# =====================================================================
# Fixtures – Ashrafi Food customizations
# (export with: bench --site af.tboss.info export-fixtures --app ashrafi_food)
# =====================================================================

AF_CUSTOM_FIELD_DOCTYPES = [
	"Address", "Asset", "Asset Repair", "Asset Value Adjustment", "Budget", "Company", "Contact",
	"Customer", "Customer Group", "Delivery Note", "Delivery Note Item", "Distribution Items",
	"Distributor Invoice", "GL Entry", "Item", "Item Group", "Journal Entry Account",
	"Landed Cost Item", "Loyalty Program", "Material Request", "Material Request Item",
	"Opening Invoice Creation Tool", "Opening Invoice Creation Tool Item", "Payment Entry",
	"Payment Entry Deduction", "POS Invoice", "POS Invoice Item", "POS Profile", "Project",
	"Purchase Invoice", "Purchase Invoice Item", "Purchase Order", "Purchase Order Item",
	"Purchase Receipt", "Purchase Receipt Item", "Purchase Taxes and Charges", "Quotation Item",
	"Sales Invoice", "Sales Invoice Item", "Sales Order", "Sales Order Item",
	"Sales Taxes and Charges", "Shipping Rule", "Stock Entry", "Stock Entry Detail",
	"Stock Reconciliation", "Subscription", "Subscription Plan", "Supplier",
	"Supplier Quotation Item", "Task", "Warehouse",
]

AF_PROPERTY_SETTER_DOCTYPES = [
	"Address", "Budget", "Bulk Payment Entry", "Customer", "Delivery Note", "Delivery Note Item",
	"Distribution Items", "Distributor Invoice", "Item", "Item Barcode", "Item Price", "Job Card",
	"Journal Entry", "Journal Entry Account", "Letter Head", "Master Shop Route",
	"Material Request", "Material Request Item", "Packed Item", "Payment Entry",
	"Payment Entry Reference", "PDC", "POS Invoice", "POS Invoice Item", "Project",
	"Purchase Invoice", "Purchase Invoice Item", "Purchase Order", "Purchase Receipt",
	"Purchase Receipt Item", "Quotation", "Sales Invoice", "Sales Invoice Item", "Sales Order",
	"Stock Entry", "Stock Entry Detail", "Stock Reconciliation", "Stock Reconciliation Item",
	"Supplier", "Supplier Quotation", "User",
]

# fields created by the Accounting Dimension "Container" (managed by ERPNext, not exported)
AF_DIMENSION_FIELDS = ["container"]

# custom field names to skip (filled later if anything overlaps with hr_vfg)
AF_EXCLUDE_CUSTOM_FIELDS = []

AF_CLIENT_SCRIPTS = [
	"Purchase Invoice-Form", "Master Shop Route-Form", "Shop Route-Form", "Sales Invoice-Form",
	"Bulk Payment Entry-Form", "Journal Entry-Form", "PDC-Form", "Material Request-Form",
	"Item-Form", "Payment Entry-Form", "Delivery Note-Form", "Stock Entry-Form",
	"Distributor Invoice-Form", "Distributor Invoice-List", "Sales Order-Form",
]

AF_SERVER_SCRIPTS = [
	"Create DI on Button Click", "Create Distributer Invoice", "DI route Name",
	"Journal Entry", "pi mob", "DI Route",
]

# non-standard (database) reports
AF_REPORTS = [
	"Damaged Item Report", "nnk", "sss", "Load Out", "Warehouse Item Qty", "Total Load Out",
	"test2", "Payment Entry", "Recovery/Current GT Report", "Recovery/Current Report",
	"Recovery Realization Report", "Accounts Receivable Report",
]

# non-standard (database) print formats
AF_PRINT_FORMATS = [
	"Purchase Order (N)", "SO", "Gate Pass", "Distributor Invoice", "CHECQUE", "Al-barka",
	"Al-barka Cheque", "JV Print format", "Metro customer", "DC for Customer",
	"Ashrafi Food Industries (DC)", "AFI Export Pay Entry", "AFI Export Sale Inc",
	"AFI Export Pur Inv", "AFI Export PI", "AFI Export PR", "AFI Export PO", "test",
	"Stock Entry New", "Bulk Payment Entry", "Payment Entry", "Payment Voucher",
	"Payment Entry Standard", "Receipt Voucher", "Purchase Invoice", "Purchase Order",
	"GRN", "Sales Tax Invoice",
]

_cf_filters = [["dt", "in", AF_CUSTOM_FIELD_DOCTYPES]]
if AF_DIMENSION_FIELDS:
	_cf_filters.append(["fieldname", "not in", AF_DIMENSION_FIELDS])
if AF_EXCLUDE_CUSTOM_FIELDS:
	_cf_filters.append(["name", "not in", AF_EXCLUDE_CUSTOM_FIELDS])

fixtures = [
	{"dt": "Custom Field",    "filters": _cf_filters},
	{"dt": "Property Setter", "filters": [["doc_type", "in", AF_PROPERTY_SETTER_DOCTYPES]]},
	{"dt": "Client Script",   "filters": [["name", "in", AF_CLIENT_SCRIPTS]]},
	{"dt": "Server Script",   "filters": [["name", "in", AF_SERVER_SCRIPTS]]},
	{"dt": "Report",          "filters": [["name", "in", AF_REPORTS]]},
	{"dt": "Print Format",    "filters": [["name", "in", AF_PRINT_FORMATS]]},
]