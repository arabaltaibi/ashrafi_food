from ashrafi_food.overrides import ACTIVE


def validate(doc, method=None):
    if not ACTIVE:
        return
    if doc.get("set_warehouse"):
        for item in doc.items:
            item.warehouse = doc.set_warehouse
