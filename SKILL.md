---
name: zoho-books
description: Zoho Books integration skill for OpenClaw (full API coverage).
metadata: {"openclaw": {"requires": {"bins": ["python3"], "env": []}}}
---

# Zoho Books Skill

## What this does
A full‑coverage Zoho Books CLI wrapper for OpenClaw. Use it to create, list, update, and manage all major accounting objects (invoices, expenses, bills, payments, banking, projects, time entries, fixed assets, etc.).

## Setup
1) Run the setup wizard:

```bash
python3 scripts/setup_wizard.py
```

2) Select the organization:

```bash
python3 scripts/zoho_books.py orgs-list
python3 scripts/zoho_books.py orgs-select --id "ORG_ID"
```

Config is stored at `~/.openclaw/zoho-books/config.json`.

## Usage (examples)

```bash
python3 scripts/zoho_books.py invoices-create --body @invoice.json
python3 scripts/zoho_books.py invoices-status-sent --id "INV_ID"
python3 scripts/zoho_books.py invoices-paymentlink --invoice-id "INV_ID" --link-type public --expiry 2026-12-31
python3 scripts/zoho_books.py invoices-payments-add --id "INV_ID" --body '{"amount":10,"payment_mode":"Cash","account_id":"ACCOUNT_ID"}'

python3 scripts/zoho_books.py expenses-create --body @expense.json --receipt /path/to/receipt.pdf
python3 scripts/zoho_books.py bills-create --body @bill.json
python3 scripts/zoho_books.py banktransactions-categorize-expenses --id "TXN_ID" --body @categorize_expense.json
```

## Notes for AI/automation
- Always ensure `organization_id` is set (use `orgs-list` + `orgs-select`).
- Use `--query` and `--body` with JSON or `@file.json` to keep inputs clean.
- Respect API limits (demo/free tiers often cap calls/day).
- For unsupported endpoints, use `request` or `upload`/`download`.

## Coverage
See **COMMAND_MATRIX.md** for the full command list and module coverage.
