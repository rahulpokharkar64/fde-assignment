try:
    from .models import Invoice
    from .respository import (
        add_invoice,
        add_payment,
        delete_invoice as repo_delete_invoice,
        delete_payment as repo_delete_payment,
        get_invoice_by_id,
        get_payment_by_id,
        update_invoice as repo_update_invoice,
        update_payment as repo_update_payment,
    )
except ImportError:  # pragma: no cover - fallback for direct script execution
    from models import Invoice
    from respository import (
        add_invoice,
        add_payment,
        delete_invoice as repo_delete_invoice,
        delete_payment as repo_delete_payment,
        get_invoice_by_id,
        get_payment_by_id,
        update_invoice as repo_update_invoice,
        update_payment as repo_update_payment,
    )


def get_invoice(invoice_id: str) -> Invoice:
    invoice_data = get_invoice_by_id(invoice_id)
    if invoice_data is not None:
        return Invoice(**invoice_data)
    raise ValueError(f"Invoice with ID {invoice_id} not found.")


def get_payment(invoice_id: str) -> Invoice:
    invoice_data = get_payment_by_id(invoice_id)
    if invoice_data is not None:
        return Invoice(**invoice_data)
    raise ValueError(f"Invoice with ID {invoice_id} not found.")


def create_invoice(invoice_data: dict) -> Invoice:
    new_invoice = Invoice(**invoice_data)
    add_invoice(new_invoice.dict())
    return new_invoice


def create_payment(invoice_data: dict) -> Invoice:
    new_invoice = Invoice(**invoice_data)
    add_payment(new_invoice.dict())
    return new_invoice


def update_invoice(invoice_id: str, updated_data: dict) -> Invoice:
    existing_invoice = get_invoice_by_id(invoice_id)
    if existing_invoice is None:
        raise ValueError(f"Invoice with ID {invoice_id} not found.")
    updated_invoice = Invoice(**updated_data)
    repo_update_invoice(invoice_id, updated_invoice.dict())
    return updated_invoice


def update_payment(invoice_id: str, updated_data: dict) -> Invoice:
    existing_payment = get_payment_by_id(invoice_id)
    if existing_payment is None:
        raise ValueError(f"Invoice with ID {invoice_id} not found.")
    updated_invoice = Invoice(**updated_data)
    repo_update_payment(invoice_id, updated_invoice.dict())
    return updated_invoice


def delete_invoice(invoice_id: str) -> None:
    existing_invoice = get_invoice_by_id(invoice_id)
    if existing_invoice is None:
        raise ValueError(f"Invoice with ID {invoice_id} not found.")
    repo_delete_invoice(invoice_id)


def delete_payment(invoice_id: str) -> None:
    existing_payment = get_payment_by_id(invoice_id)
    if existing_payment is None:
        raise ValueError(f"Invoice with ID {invoice_id} not found.")
    repo_delete_payment(invoice_id)
