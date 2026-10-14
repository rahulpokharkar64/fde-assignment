from pydantic import BaseModel


class Invoice(BaseModel):
    invoice_id: str
    vendor: str
    amount: float
    status: str | None = None
    date: str | None = None


class Payment(BaseModel):
    invoice_id: str
    paid: float