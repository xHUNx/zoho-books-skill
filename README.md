# Zoho Books OpenClaw Skill (WIP)

A full‑coverage Zoho Books integration. This repo currently contains the **OAuth setup + API client** scaffolding and will expand into complete accounting workflows.

## Quick start (OAuth)

### Option A — Setup Wizard (recommended)

```bash
python3 scripts/setup_wizard.py
```

Follow the prompts, approve the URL, paste back the code, and the config will be saved to:
`~/.openclaw/zoho-books/config.json`

Then set your org ID:

```bash
python3 scripts/zoho_books.py orgs-select --id "ORG_ID"
```

### Option B — Manual

1) Create a Zoho API client (EU default)
2) Initialize config:

```bash
python3 scripts/zoho_books.py init --dc EU
```

3) Generate consent URL:

```bash
python3 scripts/zoho_books.py auth-url --redirect-uri "https://example.com/callback"
```

4) Exchange code for refresh token:

```bash
python3 scripts/zoho_books.py exchange-code --code "YOUR_CODE" --redirect-uri "https://example.com/callback"
```

5) List organizations and select one:

```bash
python3 scripts/zoho_books.py orgs-list
python3 scripts/zoho_books.py orgs-select --id "ORG_ID"
```

6) Core commands (examples):

```bash
python3 scripts/zoho_books.py contacts-list
python3 scripts/zoho_books.py contacts-create --body @contact.json
python3 scripts/zoho_books.py contacts-get --id "CONTACT_ID"
python3 scripts/zoho_books.py contacts-activate --id "CONTACT_ID"

python3 scripts/zoho_books.py expenses-create --body @expense.json --receipt /path/to/receipt.pdf
python3 scripts/zoho_books.py expenses-list --query '{"date_start":"2024-01-01"}'

python3 scripts/zoho_books.py invoices-create --body @invoice.json
python3 scripts/zoho_books.py invoices-status-sent --id "INV_ID"
python3 scripts/zoho_books.py invoices-email --invoice-id "INV_ID" --body @invoice_email.json

python3 scripts/zoho_books.py bills-create --body @bill.json
python3 scripts/zoho_books.py bills-approve --id "BILL_ID"

python3 scripts/zoho_books.py banktransactions-list --query '{"status":"uncategorized"}'
python3 scripts/zoho_books.py banktransactions-match --transaction-id "TXN_ID" --body @match.json
python3 scripts/zoho_books.py banktransactions-unmatch --id "TXN_ID"

python3 scripts/zoho_books.py projects-create --body @project.json
python3 scripts/zoho_books.py tasks-list --project-id "PROJ_ID"
python3 scripts/zoho_books.py timeentries-timer-start --id "TIME_ID"
```

## Config
Stored at: `~/.openclaw/zoho-books/config.json`

```json
{
  "datacenter": "EU",
  "client_id": "",
  "client_secret": "",
  "redirect_uri": "",
  "refresh_token": "",
  "organization_id": ""
}
```

## Status
OAuth scaffold complete. Core CRUD + actions added for major accounting modules (invoices, expenses, bills, contacts, items, bank accounts/transactions, estimates, sales/purchase orders, credit notes, retainer invoices, projects/tasks/time entries, taxes, journals). Continue expanding to full module coverage and advanced actions.
