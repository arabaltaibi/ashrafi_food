import json
import os

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field


def sync():
"""Re-create fields that were added directly to ERPNext v13 core files.
Skips any field the doctype already has (so it does nothing on v13)."""
path = os.path.join(os.path.dirname(__file__), "v13_core_fields.json")
with open(path) as f:
fields = json.load(f)

created = []
for df in fields:
df = dict(df)
dt = df.pop("dt")
if not frappe.db.exists("DocType", dt):
continue
if frappe.get_meta(dt, cached=False).has_field(df["fieldname"]):
continue
create_custom_field(dt, df, ignore_validate=True)
created.append(f"{dt}.{df['fieldname']}")

if created:
frappe.db.commit()
print("ashrafi_food: created custom fields:", ", ".join(created))
