# FixBill

AI invoice assistant for freelance PC and network installers.

A technician types a plain job note — "Installed 3 access points, ran 40m of
cable, 2 days on site, supplied a switch" — the app drafts structured invoice
line items with suggested price ranges, the technician edits them, then the
app creates a real PayPal invoice (sandbox) and payment link. Payment is the
product, not a bolt-on.

Built for the PayPal AI Hackathon 2026. Sandbox only — no real money.

## Run it

```bash
cp .env.example .env   # fill in your sandbox Client ID / Secret
pip install -r requirements.txt
python3 scripts/test_sandbox.py   # Day 1 gate: token + draft invoice
uvicorn app.main:app --reload
```

## Licence

MIT — see LICENSE.
