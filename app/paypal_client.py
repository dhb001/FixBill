"""PayPal sandbox client for FixBill — stdlib only, no extra dependency.

Verified against PayPal Developer Invoices v2 (checked 2026-11-07):
  token:  POST https://api-m.sandbox.paypal.com/v1/oauth2/token
          grant_type=client_credentials, Basic auth client_id:secret
  create: POST https://api-m.sandbox.paypal.com/v2/invoicing/invoices
          -> draft invoice, returns id (e.g. INV2-...) and status DRAFT
  send:   POST https://api-m.sandbox.paypal.com/v2/invoicing/invoices/{id}/send
  read:   GET  https://api-m.sandbox.paypal.com/v2/invoicing/invoices/{id}

Sandbox only. Never point this at api-m.paypal.com for the hackathon.
"""
import base64
import json
import os
import urllib.request

SANDBOX_BASE = "https://api-m.sandbox.paypal.com"


def _env(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"missing env var {name} — copy .env.example to .env first")
    return value


def get_access_token():
    client_id = _env("PAYPAL_CLIENT_ID")
    secret = _env("PAYPAL_CLIENT_SECRET")
    basic = base64.b64encode(f"{client_id}:{secret}".encode()).decode()
    req = urllib.request.Request(
        f"{SANDBOX_BASE}/v1/oauth2/token",
        data=b"grant_type=client_credentials",
        headers={
            "Authorization": f"Basic {basic}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)["access_token"]


def _call(method, path, token, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        f"{SANDBOX_BASE}{path}",
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method=method,
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def create_draft_invoice(token, payer_email, items, currency="USD", note=""):
    """items: [{description, quantity, unit_amount}] — unit_amount is a string like "45.00"."""
    payload = {
        "detail": {
            "currency_code": currency,
            "note": note or "FixBill sandbox test invoice — no real money.",
        },
        "invoicer": {"name": {"given_name": "FixBill", "surname": "Sandbox"}},
        "primary_recipients": [{"billing_info": {"email_address": payer_email}}],
        "items": [
            {
                "name": it["description"][:100],
                "description": it["description"],
                "quantity": str(it["quantity"]),
                "unit_amount": {"currency_code": currency, "value": str(it["unit_amount"])},
            }
            for it in items
        ],
    }
    return _call("POST", "/v2/invoicing/invoices", token, payload)


def get_invoice(token, invoice_id):
    return _call("GET", f"/v2/invoicing/invoices/{invoice_id}", token)


def send_invoice(token, invoice_id):
    return _call("POST", f"/v2/invoicing/invoices/{invoice_id}/send", token, {})
