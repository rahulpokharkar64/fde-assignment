import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE_INVOICES = BASE_DIR / "invoice.json"
DATA_FILE_PAYMENTS = BASE_DIR / "payments.json"


# Load files from the current assignment folder only.
def load_invoices():
    with open(DATA_FILE_INVOICES, "r", encoding="utf-8") as f:
        return json.load(f)


def load_payments():
    with open(DATA_FILE_PAYMENTS, "r", encoding="utf-8") as f:
        return json.load(f)


# Save invoice/payments

def save_invoices(invoices):
    with open(DATA_FILE_INVOICES, "w", encoding="utf-8") as f:
        json.dump(invoices, f, indent=4)


def save_payments(payments):
    with open(DATA_FILE_PAYMENTS, "w", encoding="utf-8") as f:
        json.dump(payments, f, indent=4)


# Get invoices and payments

def get_invoice_by_id(invoice_id):
    invoices = load_invoices()
    for invoice in invoices:
        if invoice["invoice_id"] == invoice_id:
            return invoice
    return None


def get_payment_by_id(invoice_id):
    invoices = load_payments()
    for invoice in invoices:
        if invoice["invoice_id"] == invoice_id:
            return invoice
    return None


# Add invoices / payments

def add_invoice(invoice):
    invoices = load_invoices()
    invoices.append(invoice)
    save_invoices(invoices)


def add_payment(payment):
    payments = load_payments()
    payments.append(payment)
    save_payments(payments)


# Update invoices/payments

def update_invoice(invoice_id, updated_invoice):
    invoices = load_invoices()
    for i, invoice in enumerate(invoices):
        if invoice["invoice_id"] == invoice_id:
            invoices[i] = updated_invoice
            save_invoices(invoices)
            return True
    return False


def update_payment(invoice_id, updated_invoice):
    payments = load_payments()
    for i, payment in enumerate(payments):
        if payment["invoice_id"] == invoice_id:
            payments[i] = updated_invoice
            save_payments(payments)
            return True
    return False


def delete_invoice(invoice_id):
    invoices = load_invoices()
    invoices = [invoice for invoice in invoices if invoice["invoice_id"] != invoice_id]
    save_invoices(invoices)


def delete_payment(invoice_id):
    payments = load_payments()
    payments = [payment for payment in payments if payment["invoice_id"] != invoice_id]
    save_payments(payments)

