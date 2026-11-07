"""Day 1 smoke test — PayPal sandbox go/no-go gate.

Run:  cp .env.example .env   # then fill in sandbox Client ID / Secret
      python3 scripts/test_sandbox.py

PASS = token obtained + draft invoice created (status DRAFT) + read back.
FAIL = any exception. If it fails after ~2h of trying, the gate says DROP.
Creates ONE draft invoice only. Never sends it, never takes payment.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import paypal_client  # noqa: E402

EXAMPLE_ITEMS = [
    {"description": "Access point — supply and install", "quantity": 3, "unit_amount": "60.00"},
    {"description": "Network cable run", "quantity": 40, "unit_amount": "2.00"},
    {"description": "On-site labour", "quantity": 2, "unit_amount": "45.00"},
    {"description": "Network switch — supplied", "quantity": 1, "unit_amount": "80.00"},
]


def main():
    payer = os.environ.get("PAYPAL_SANDBOX_PAYER_EMAIL", "").strip()
    if not payer:
        print("FAIL: set PAYPAL_SANDBOX_PAYER_EMAIL in .env (sandbox Personal test account email)")
        return 1
    try:
        token = paypal_client.get_access_token()
        print("token: OK")
        invoice = paypal_client.create_draft_invoice(token, payer, EXAMPLE_ITEMS)
        invoice_id = invoice.get("id")
        print(f"created: {invoice_id} status={invoice.get('status')}")
        back = paypal_client.get_invoice(token, invoice_id)
        print(f"read back: {back.get('id')} status={back.get('status')}")
        if back.get("status") != "DRAFT":
            print(f"FAIL: expected DRAFT, got {back.get('status')}")
            return 1
        print("DAY 1 GATE: PASS — sandbox works, proceed to Day 2")
        return 0
    except Exception as exc:  # noqa: BLE001 — smoke test: report, don't crash silently
        print(f"FAIL: {type(exc).__name__}: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
