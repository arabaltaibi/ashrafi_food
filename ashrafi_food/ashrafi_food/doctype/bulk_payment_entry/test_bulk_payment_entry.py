import frappe
@frappe.whitelist()
def create_payment_entry(posting_date, mode_of_payment, ref_no, ref_date, paid_amount,party,account_paid_from,paid_to_account_currency,received_amount,target_exchange_rate):
  # Create a new Payment Entry document

  doc = frappe.new_doc('Payment Entry')
  doc.payment_type="Pay"
  doc.posting_date = posting_date
  doc.mode_of_payment = mode_of_payment
  doc.reference_no = ref_no
  doc.reference_date = ref_date
  doc.paid_amount = paid_amount
  doc.party=party
  doc.party_type="Supplier"
  doc.received_amount=received_amount
  doc.target_exchange_rate= target_exchange_rate
  doc.source_exchange_rate= target_exchange_rate
  doc.paid_to_account_currency=paid_to_account_currency
  doc.paid_from=account_paid_from
  doc.bill_type="Current Bill"

  
  doc.save()

  doc.submit()
  frappe.msgprint("Payment Entry created successfully!")
  return {"message": "Payment Entry created successfully!"}
