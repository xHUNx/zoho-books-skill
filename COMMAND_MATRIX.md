# Zoho Books Command Matrix (WIP)

Generated from MODULES.md — fill in concrete CLI commands per module.

## Bank Accounts

- list
- get
- create
- update
- delete
- actions: activate, deactivate

## Bank Rules

- list
- get
- create
- update
- delete
- actions: (none)

## Bank Transactions

- list
- get
- create
- update
- delete
- actions: match, unmatch, uncategorize

## Base Currency Adjustment

- list
- get
- create
- update
- delete
- actions: (none)

## Bills

- list
- get
- create
- update
- delete
- actions: status-open, status-void, submit, approve, comments-list/add/delete, attach, payments-list/add/get/delete

## Chart Of Accounts

- list
- get
- create
- update
- delete
- actions: activate, deactivate

## Contact Persons

- list
- get
- create
- update
- delete
- actions: (none)

## Contacts

- list
- get
- create
- update
- delete
- actions: activate, deactivate, portal-enable

## Credit Notes

- list
- get
- create
- update
- delete
- actions: status-void, status-draft, status-open, submit, approve, email, comments-list/add/delete, templates-list/apply, refunds-list/add/get/update/delete

## Currency

- list
- get
- create
- update
- delete
- actions: (none)

## Custom Modules

- list
- get
- create
- update
- delete
- actions: (custom module name via path; not wired)

## Customer Debit Notes

- list
- get
- create
- update
- delete
- actions: (not wired yet)

## Customer Payments

- list
- get
- create
- update
- delete
- actions: refunds-list/add/get/update/delete

## Estimates

- list
- get
- create
- update
- delete
- actions: status-sent, status-accepted, status-declined, submit, approve, email, comments-list/add/delete, templates-list/apply

## Expenses

- list
- get
- create
- update
- delete
- actions: comments-list, receipt/attachment (create)

## Fixed Assets

- list
- get
- create
- update
- delete
- actions: (none)

## ZOHO CRM Integration

- list
- get
- create
- update
- delete
- actions: (status/email/submit/approve/etc — fill per module)

## Invoices

- list
- get
- create
- update
- delete
- actions: status-sent, status-void, status-draft, submit, approve, paymentreminder-enable, paymentreminder-disable, writeoff, writeoff-cancel, email, comments-list/add/delete, attach, templates-list/apply, payments-list/add/get/delete

## Items

- list
- get
- create
- update
- delete
- actions: activate, deactivate

## Journals

- list
- get
- create
- update
- delete
- actions: publish, comments-list/add/delete, attach

## Locations

- list
- get
- create
- update
- delete
- actions: enable, activate, deactivate, mark-primary

## Opening Balance

- list
- get
- create
- update
- delete
- actions: (none)

## Organizations

- list
- get
- create
- update
- delete
- actions: (list/get wired; create/update/delete not wired)

## Projects

- list
- get
- create
- update
- delete
- actions: activate, deactivate, clone

## Purchase Order

- list
- get
- create
- update
- delete
- actions: status-open, status-billed, status-cancelled, submit, approve, email, reject, comments-list/add/delete, attach, templates-list/apply

## Recurring Bills

- list
- get
- create
- update
- delete
- actions: (none)

## Recurring Expenses

- list
- get
- create
- update
- delete
- actions: (none)

## Recurring Invoices

- list
- get
- create
- update
- delete
- actions: (none)

## Reporting Tags

- list
- get
- create
- update
- delete
- actions: mark-default

## Retainer Invoices

- list
- get
- create
- update
- delete
- actions: status-sent, status-void, status-draft, submit, approve, email, comments-list/add/delete, attach, templates-list/apply

## Sales Order

- list
- get
- create
- update
- delete
- actions: status-open, status-void, submit, approve, email, comments-list/add/delete, attach, templates-list/apply

## Sales Receipt

- list
- get
- create
- update
- delete
- actions: (none)

## Tasks

- list (by project_id)
- get
- create
- update
- delete
- actions: (none yet)

## Taxes

- list
- get
- create
- update
- delete
- actions: (taxgroups, taxauthorities, taxexemptions supported as separate modules)

## Time Entries

- list
- get
- create
- update
- delete
- actions: timer-start, timer-stop, timer-running

## Users

- list
- get
- create
- update
- delete
- actions: (none)

## Vendor Credits

- list
- get
- create
- update
- delete
- actions: status-open, status-void, submit, approve, comments-list/add/delete, refunds-list/add/get/update/delete

## Vendor Payments

- list
- get
- create
- update
- delete
- actions: email, refunds-list/add/get/update/delete
