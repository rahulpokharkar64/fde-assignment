from fastapi import FastAPI, HTTPException

try:
    from .models import Invoice
    from .services import (
        create_invoice,
        create_payment,
        delete_invoice,
        delete_payment,
        get_invoice,
        get_payment,
        update_invoice,
        update_payment,
    )
except ImportError:  # pragma: no cover - fallback for direct script execution
    from models import Invoice
    from services import (
        create_invoice,
        create_payment,
        delete_invoice,
        delete_payment,
        get_invoice,
        get_payment,
        update_invoice,
        update_payment,
    )

app = FastAPI()


@app.get("/invoices/{invoice_id}", response_model=Invoice)
def read_invoice(invoice_id: str):
    try:
        return get_invoice(invoice_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/invoices/", response_model=Invoice)
def create_new_invoice(invoice: Invoice):
    return create_invoice(invoice.dict())


@app.put("/invoices/{invoice_id}", response_model=Invoice)
def update_existing_invoice(invoice_id: str, updated_invoice: Invoice):
    try:
        return update_invoice(invoice_id, updated_invoice.dict())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/invoices/{invoice_id}")
def delete_existing_invoice(invoice_id: str):
    try:
        delete_invoice(invoice_id)
        return {"message": f"Invoice with ID {invoice_id} deleted successfully."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/payments/{invoice_id}", response_model=Invoice)
def read_payment(invoice_id: str):
    try:
        return get_payment(invoice_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/payments/", response_model=Invoice)
def create_new_payment(invoice: Invoice):
    return create_payment(invoice.dict())


@app.put("/payments/{invoice_id}", response_model=Invoice)
def update_existing_payment(invoice_id: str, updated_invoice: Invoice):
    try:
        return update_payment(invoice_id, updated_invoice.dict())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/payments/{invoice_id}")
def delete_existing_payment(invoice_id: str):
    try:
        delete_payment(invoice_id)
        return {"message": f"Invoice with ID {invoice_id} deleted successfully."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


if __name__ == "__main__":
    try:
        import uvicorn
    except ModuleNotFoundError:
        print("uvicorn is not installed. Install it with: pip install uvicorn")
    else:
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)