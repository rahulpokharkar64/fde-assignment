from fastapi import APIRouter
from data_store import invoices
router = APIRouter()

@router.get("/invoices")
def get_invoices():
    return invoices

@router.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: int):
    invoice = next((inv for inv in invoices if inv["id"] == invoice_id), None)
    if invoice:
        return invoice
    else:
        return {"error": "Invoice not found"}