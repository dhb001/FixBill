"""FixBill — AI invoice assistant for freelance PC/network installers.

Day 1 scope: health check, job-note -> draft line items, PayPal sandbox
draft invoice. No AI call yet (Day 2), no send/payment yet (Day 3–4).
Run:  uvicorn app.main:app --reload   (from the repo root, after .env)
"""
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.draft import draft_from_note
from app import paypal_client

app = FastAPI(title="FixBill", version="0.1.0-day1")


class DraftRequest(BaseModel):
    note: str


class InvoiceRequest(BaseModel):
    payer_email: str
    items: list  # [{description, quantity, unit_amount}]
    currency: str = "USD"


@app.get("/health")
def health():
    return {"status": "ok", "env": "sandbox"}


@app.post("/draft")
def draft(req: DraftRequest):
    """Job note -> suggested line items. Technician edits before invoicing."""
    if not req.note.strip():
        raise HTTPException(status_code=400, detail="note is empty")
    return draft_from_note(req.note)


@app.post("/invoices")
def create_invoice(req: InvoiceRequest):
    """Create a PayPal sandbox DRAFT invoice from edited line items."""
    if not req.items:
        raise HTTPException(status_code=400, detail="no line items")
    token = paypal_client.get_access_token()
    invoice = paypal_client.create_draft_invoice(
        token, req.payer_email, req.items, currency=req.currency
    )
    return {
        "invoice_id": invoice.get("id"),
        "status": invoice.get("status"),
        "detail": invoice.get("detail", {}),
        "links": invoice.get("links", []),
    }


@app.get("/invoices/{invoice_id}")
def read_invoice(invoice_id: str):
    token = paypal_client.get_access_token()
    return paypal_client.get_invoice(token, invoice_id)
