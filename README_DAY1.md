# FixBill — Day 1 starter kit (PayPal AI Hackathon)
Prepared 2026-11-07 ~08:45 EAT, before any build decision. Nothing here has been
pushed, published, or run against PayPal — there are no credentials in this kit.
If Dhruvin says DROP, delete this folder; nothing is lost.

## What Day 1 has to prove (go / no-go gate)
By end of today (Sat 7 Nov 2026), all three must be true, or drop the entry:
1. A PayPal Developer sandbox app exists and returns an access token.
2. A draft invoice is created in sandbox via `POST /v2/invoicing/invoices`
   and can be read back (status DRAFT).
3. The repo skeleton below runs locally (`uvicorn app.main:app`) and its
   `/health` endpoint answers.

If any of the three stalls for more than ~2 hours of trying, stop — that is the
gate doing its job. Do not burn Days 2–3 on a broken sandbox.

## Exact sandbox steps (all in the browser, ~20 min)
1. Go to https://developer.paypal.com/ and log in with a PayPal account.
2. Dashboard → My Apps & Credentials → Sandbox tab → Create App.
   Name it `FixBill`, merchant type: Merchant.
3. Copy the sandbox **Client ID** and **Secret** into `.env` (see `.env.example`).
   Never commit `.env`. Sandbox credentials only — no real money, ever.
4. In the same dashboard, check the sandbox test accounts: one Business
   (merchant, receives the invoice) and one Personal (payer, pays it).
   Note the payer's sandbox email — it is the `primary_recipients` address
   used in the test invoice.
5. Run the smoke test: `python3 scripts/test_sandbox.py`
   It gets a token, creates one draft invoice for the example job
   ("Installed 3 access points, ran 40m of cable, 2 days on site, supplied
   a switch"), prints the invoice ID + status, then reads it back.
   It does NOT send the invoice and does NOT take any payment.

## Files in this kit
- `app/main.py` — FastAPI app: `/health`, `/draft` (job note → line items,
  rule-based parser now, one AI call to be wired on Day 2), `/invoices`
  (create a PayPal draft invoice from edited line items).
- `app/paypal_client.py` — sandbox token + create/read invoice, stdlib only.
- `app/draft.py` — parses quantities out of a plain job note
  ("3 access points", "40m of cable", "2 days on site", "a switch").
  Prices are SUGGESTED RANGES the technician must edit — no rate card is
  baked in, per the concept doc.
- `scripts/test_sandbox.py` — the Day 1 smoke test above.
- `requirements.txt`, `.env.example`, `README.md` (repo-ready, MIT note),
  `LICENSE` (MIT, Copyright (c) 2026 Dhruvin Hitesh Bhudia — same licence
  choice as NANFO, 2026-11-06).

## Day 2–3 preview (only if Day 1 passes)
Wire one AI call into `/draft` (job note → line items + price ranges),
add a tiny edit screen, then the pay-link flow (`/send` on the invoice).
Day 4: reconciliation + receipt. Day 5: <3 min video + README + submission
text. Day 6 (Thu 12 Nov): submit before 23:00 EAT.

## Sources verified 2026-11-07
- PayPal Developer, Invoices v2 reference: create draft invoice
  `POST /v2/invoicing/invoices`, send `POST /v2/invoicing/invoices/{id}/send`,
  sandbox base `https://api-m.sandbox.paypal.com`, token
  `POST /v1/oauth2/token` with `grant_type=client_credentials`.
  https://developer.paypal.com/api/invoicing/v2
- Concept + deadlines: `../paypal-entry-concept.md` in this goal folder
  (submissions close Thu 12 Nov 2026, 23:00 EAT; prize pool $69,750).
