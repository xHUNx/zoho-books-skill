# Zoho Books Skill — Design & Architecture (Snapshot)

## Goal
Create a full‑coverage Zoho Books OpenClaw skill that can act as a virtual accountant: handle expenses (with receipt image uploads), invoices, bank transaction matching, bills, credits, payments, reporting, etc. Must support *all* Zoho Books modules exposed by the API. Default data center: **EU**, but configurable to **US/IN/AU/JP** during setup.

## Inputs
- OpenAPI specs in `openapi-all/*.yml`
- Official docs (examples):
  - https://www.zoho.com/books/api/v3/introduction/
  - https://www.zoho.com/books/api/v3/oauth/#overview

## Core API Patterns (from spec)
- Base URL: `https://www.zohoapis.com/books/v3`
- **All requests require `organization_id`** query param.
- OAuth scopes per module (examples):
  - `ZohoBooks.settings.*` for organizations
  - `ZohoBooks.expenses.*`
  - `ZohoBooks.invoices.*`
  - `ZohoBooks.banking.*`
- OAuth security scheme in OpenAPI uses Zoho_Auth.

## Modules Present (OpenAPI)
A non‑exhaustive list already mapped:
- organizations
- expenses (receipt attach, comments, employees)
- invoices (emailing, attachments, templates, reminders, payments, credits)
- bank-transactions (categorize/match/uncategorize)

Remaining modules in `openapi-all` still to map into full matrix:
- bank-accounts, bank-rules
- bills, vendor‑credits, vendor‑payments, customer‑payments, credit‑notes
- contacts, contact‑persons, items, taxes, currencies, chart‑of‑accounts
- estimates, sales‑orders, purchase‑orders, retainer‑invoices
- projects, tasks, time‑entries
- recurring‑* (bills/expenses/invoices)
- journals, fixed‑assets, reporting‑tags, locations, users
- integration, organizations, opening‑balance, base‑currency‑adjustment

## Skill Architecture (Proposed)
- **Config**:
  - `ZOHO_DATACENTER` (EU default; supports US/IN/AU/JP)
  - OAuth client_id/client_secret, refresh token, access token caching
  - `ZOHO_ORG_ID` (or select from `/organizations`)
- **HTTP Client**: generic wrapper with:
  - base URL derived from datacenter
  - auto‑refresh token
  - inject org_id per request
  - retry/backoff (respect 1000/day limit)
- **Actions**: expose human‑level commands (create invoice, expense from receipt, match bank transaction, etc.)
- **Attachment uploads**:
  - `multipart/form-data` endpoints for receipts/attachments
  - local file path → attach
- **Receipts to Expense** flow:
  1. Extract fields (vendor, amount, date) from image (OCR) — optional
  2. POST `/expenses` with receipt upload
  3. Confirm created expense + receipt attached

## Immediate Next Steps
1) Parse all `openapi-all/*.yml` to build module → endpoints → required scopes matrix.
2) Draft skill README + SKILL.md for Zoho Books.
3) Implement OAuth helper + datacenter configuration (EU default).
4) Create minimal CLI functions (list orgs, list contacts, create expense, create invoice) for test.
5) Validate against demo org once user provides.

## Notes
- Free tier API limit: 1000 calls/day → add caching + avoid retries.
- For image → expense: optionally use OCR (future add). For now, attach and let user input fields.
- Bank transaction matching uses `/banktransactions/uncategorized/{id}/match` and related endpoints.
