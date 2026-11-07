"""Job-note -> draft line items.

Day 1: deterministic parser only — pulls quantities out of plain English
("3 access points", "40m of cable", "2 days on site", "a switch").
Day 2: one AI call replaces/augments this, keeping the same output shape;
the technician always edits before anything is sent to PayPal.

Prices are SUGGESTED RANGES, not a rate card. Every item carries
low/high so the UI can show "suggested KES/USD X–Y, edit me".
Currency is USD in sandbox (PayPal sandbox default); the technician's
local currency choice is a Day 2 decision, not baked in here.
"""
import re

_PATTERNS = [
    # (regex, description template, unit, suggested low, suggested high)
    (r"(\d+)\s+access points?", "Access point — supply and install", "each", 45, 80),
    (r"(\d+)\s*m(?:etres|eters)?\s+of\s+cable", "Network cable run", "per metre", 1, 3),
    (r"(\d+)\s+days?\s+on\s+site", "On-site labour", "per day", 30, 60),
    (r"(?:supplied|supply)\s+a\s+switch", "Network switch — supplied", "each", 40, 120),
    (r"(\d+)\s+switch(?:es)?", "Network switch — supplied", "each", 40, 120),
]


def draft_from_note(note: str):
    """Return {'line_items': [...], 'unparsed': [...]}.

    line_item: {description, quantity, unit, suggested_low, suggested_high}
    """
    text = (note or "").strip()
    items = []
    covered = []
    for pattern, desc, unit, low, high in _PATTERNS:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            qty = int(m.group(1)) if m.groups() and m.group(1) and m.group(1).isdigit() else 1
            items.append({
                "description": desc,
                "quantity": qty,
                "unit": unit,
                "suggested_low": low,
                "suggested_high": high,
            })
            covered.append(m.group(0))
    unparsed = text
    for chunk in covered:
        unparsed = unparsed.replace(chunk, "", 1)
    unparsed = re.sub(r"[,;]\s*", " ", unparsed).strip(" .")
    return {"line_items": items, "unparsed": unparsed}
