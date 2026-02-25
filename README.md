# Zoho Books OpenClaw Skill (WIP)

A full‑coverage Zoho Books integration. This repo currently contains the **OAuth setup + API client** scaffolding and will expand into complete accounting workflows.

## Quick start (OAuth)

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

python3 scripts/zoho_books.py expenses-create --body @expense.json --receipt /path/to/receipt.pdf
python3 scripts/zoho_books.py invoices-create --body @invoice.json
python3 scripts/zoho_books.py invoices-email --invoice-id "INV_ID" --body @invoice_email.json

python3 scripts/zoho_books.py banktransactions-list --query '{"status":"uncategorized"}'
python3 scripts/zoho_books.py banktransactions-match --transaction-id "TXN_ID" --body @match.json
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
OAuth scaffold complete. Next: module map + workflows + expense/invoice/banking commands.
