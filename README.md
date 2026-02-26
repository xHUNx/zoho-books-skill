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
python3 scripts/zoho_books.py invoices-comments-add --id "INV_ID" --body @comment.json
python3 scripts/zoho_books.py invoices-attach --id "INV_ID" --file /path/to/file.pdf
python3 scripts/zoho_books.py invoices-pdf --query '{"invoice_ids":"INV_ID"}' --out invoice.pdf
python3 scripts/zoho_books.py invoices-paymentlink --invoice-id "INV_ID" --link-type public --expiry 2026-12-31
python3 scripts/zoho_books.py invoices-payments-add --id "INV_ID" --body '{"amount":10,"payment_mode":"Cash","account_id":"ACCOUNT_ID"}'

python3 scripts/zoho_books.py bills-create --body @bill.json
python3 scripts/zoho_books.py bills-approve --id "BILL_ID"
python3 scripts/zoho_books.py bills-attach --id "BILL_ID" --file /path/to/file.pdf

python3 scripts/zoho_books.py banktransactions-list --query '{"status":"uncategorized"}'
python3 scripts/zoho_books.py banktransactions-match --transaction-id "TXN_ID" --body @match.json
python3 scripts/zoho_books.py banktransactions-unmatch --id "TXN_ID"

python3 scripts/zoho_books.py projects-create --body @project.json
python3 scripts/zoho_books.py tasks-list --project-id "PROJ_ID"
python3 scripts/zoho_books.py timeentries-timer-start --id "TIME_ID"

# Generic file upload / download
python3 scripts/zoho_books.py upload --path "/invoices/INV_ID/attachment" --file /path/to/file.pdf
python3 scripts/zoho_books.py download --path "/invoices/pdf" --query '{"invoice_id":"INV_ID"}' --out invoice.pdf

# Custom modules
python3 scripts/zoho_books.py custommodules-list --module cm_debtor
python3 scripts/zoho_books.py custommodules-create --module cm_debtor --body @custom_record.json

# Bank transaction categorization
python3 scripts/zoho_books.py banktransactions-categorize-expenses --id "TXN_ID" --body @categorize_expense.json

# Bank statements
python3 scripts/zoho_books.py bankstatements-import --body @statement.json
python3 scripts/zoho_books.py bankaccounts-lastimported --account-id "ACC_ID"

# Customer debit note (uses /invoices with type=debit_note; must reference a non-draft invoice)
python3 scripts/zoho_books.py debitnotes-create --body '{"customer_id":"CUST_ID","reference_invoice_id":"INV_ID","line_items":[{"description":"Adjustment","rate":2,"quantity":1,"account_id":"ACCOUNT_ID"}]}'

# Reporting tags (minimal example)
python3 scripts/zoho_books.py reportingtags-create --body '{"tag_name":"QA Tag","entities":[{"entity_name":"customers","is_enabled":true}],"multi_preference_entities":{"preference":"line_item","entities":[{"entity_name":"sales","is_enabled":true}]},"tag_options":[{"tag_option_name":"A"},{"tag_option_name":"B"}]}'
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
OAuth scaffold complete. Core CRUD + actions added for major accounting modules (invoices, expenses, bills, contacts, items, bank accounts/transactions, estimates, sales/purchase orders, credit notes, retainer invoices, vendor credits/payments, projects/tasks/time entries, taxes, journals) plus remaining modules (bank rules, base currency adjustment, contact persons, currencies, fixed assets, locations, opening balances, recurring bills/expenses/invoices, reporting tags, sales receipts, users). Continue expanding advanced actions and custom module handling.
