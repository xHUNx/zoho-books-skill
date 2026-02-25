---
name: zoho-books
description: Zoho Books integration skill (WIP). OAuth setup + API client scaffolding with full module coverage planned.
metadata: {"openclaw":{"requires":{"bins":["python3"],"env":[]}}}
---

# Zoho Books Skill (WIP)

## Quick start

```bash
python3 scripts/zoho_books.py init --dc EU
python3 scripts/zoho_books.py auth-url --redirect-uri "https://example.com/callback"
```

## Notes
- Default data center: EU (configurable)
- Uses OAuth refresh tokens
- Core commands implemented: orgs, contacts, expenses (with receipt), invoices (create/email), bank transactions (list/match)
- Full module map + workflows continue next
