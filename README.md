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

5) List organizations:

```bash
python3 scripts/zoho_books.py request --method GET --path /organizations
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
