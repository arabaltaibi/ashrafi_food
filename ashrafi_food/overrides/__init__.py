import erpnext

# ERPNext v13 still has these customizations inside its own core files,
# so the hooks in this package only act on v14 and later.
ERPNEXT_MAJOR = int(erpnext.__version__.split(".")[0])
ACTIVE = ERPNEXT_MAJOR >= 14
