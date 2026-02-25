# Zoho Books API Modules (from openapi-all)

Source: /Users/dandan/.openclaw/workspace-donna/openapi-all

## Bank Accounts (7)
File: `bank-accounts.yml`

Endpoints:
- `/bankaccounts`
- `/bankaccounts/{account_id}`
- `/bankaccounts/{account_id}/inactive`
- `/bankaccounts/{account_id}/active`
- `/bankstatements`
- `/bankaccounts/{account_id}/statement/lastimported`
- `/bankaccounts/{account_id}/statement/{statement_id}`

## Bank Rules (2)
File: `bank-rules.yml`

Endpoints:
- `/bankaccounts/rules`
- `/bankaccounts/rules/{rule_id}`

## Bank Transactions (15)
File: `bank-transactions.yml`

Endpoints:
- `/banktransactions`
- `/banktransactions/{bank_transaction_id}`
- `/banktransactions/uncategorized/{transaction_id}/match`
- `/banktransactions/{transaction_id}/unmatch`
- `/banktransactions/uncategorized/{transaction_id}/exclude`
- `/banktransactions/uncategorized/{transaction_id}/restore`
- `/banktransactions/uncategorized/{transaction_id}/categorize`
- `/banktransactions/uncategorized/{transaction_id}/categorize/expenses`
- `/banktransactions/{transaction_id}/uncategorize`
- `/banktransactions/uncategorized/{transaction_id}/categorize/vendorpayments`
- `/banktransactions/uncategorized/{transaction_id}/categorize/customerpayments`
- `/banktransactions/uncategorized/{transaction_id}/categorize/creditnoterefunds`
- `/banktransactions/uncategorized/{transaction_id}/categorize/vendorcreditrefunds`
- `/banktransactions/uncategorized/{statement_line_id}/categorize/paymentrefunds`
- `/banktransactions/uncategorized/{statement_line_id}/categorize/vendorpaymentrefunds`

## Base Currency Adjustment (3)
File: `base-currency-adjustment.yml`

Endpoints:
- `/basecurrencyadjustment`
- `/basecurrencyadjustment/{base_currency_adjustment_id}`
- `/basecurrencyadjustment/accounts`

## Bills (15)
File: `bills.yml`

Endpoints:
- `/bills`
- `/bills/{bill_id}`
- `/bill/{bill_id}/customfields`
- `/bills/{bill_id}/status/void`
- `/bills/{bill_id}/status/open`
- `/bills/{bill_id}/submit`
- `/bills/{bill_id}/approve`
- `/bills/{bill_id}/address/billing`
- `/bills/{bill_id}/payments`
- `/bills/{bill_id}/credits`
- `/bills/{bill_id}/payments/{bill_payment_id}`
- `/bills/{bill_id}/attachment`
- `/bills/{bill_id}/comments`
- `/bills/{bill_id}/comments/{comment_id}`
- `/bills/editpage/frompurchaseorders`

## Chart Of Accounts (6)
File: `chart-of-accounts.yml`

Endpoints:
- `/chartofaccounts`
- `/chartofaccounts/{account_id}`
- `/chartofaccounts/{account_id}/active`
- `/chartofaccounts/{account_id}/inactive`
- `/chartofaccounts/transactions`
- `/chartofaccounts/transactions/{transaction_id}`

## Contact Persons (5)
File: `contact-persons.yml`

Endpoints:
- `/contacts/contactpersons`
- `/contacts/contactpersons/{contact_person_id}`
- `/contacts/{contact_id}/contactpersons`
- `/contacts/{contact_id}/contactpersons/{contact_person_id}`
- `/contacts/contactpersons/{contact_person_id}/primary`

## Contacts (16)
File: `contacts.yml`

Endpoints:
- `/contacts`
- `/contacts/{contact_id}`
- `/contacts/{contact_id}/active`
- `/contacts/{contact_id}/inactive`
- `/contacts/{contact_id}/portal/enable`
- `/contacts/{contact_id}/paymentreminder/enable`
- `/contacts/{contact_id}/paymentreminder/disable`
- `/contacts/{contact_id}/statements/email`
- `/contacts/{contact_id}/email`
- `/contacts/{contact_id}/comments`
- `/contacts/{contact_id}/address`
- `/contacts/{contact_id}/address/{address_id}`
- `/contacts/{contact_id}/refunds`
- `/contacts/{contact_id}/track1099`
- `/contacts/{contact_id}/untrack1099`
- `/contacts/{contact_id}/receivables/unusedretainerpayments`

## Credit Notes (20)
File: `credit-notes.yml`

Endpoints:
- `/creditnotes`
- `/creditnotes/{creditnote_id}`
- `/creditnotes/{creditnote_id}/email`
- `/creditnotes/{creditnote_id}/status/void`
- `/creditnotes/{creditnote_id}/status/draft`
- `/creditnotes/{creditnote_id}/status/open`
- `/creditnotes/{creditnote_id}/submit`
- `/creditnotes/{creditnote_id}/approve`
- `/creditnotes/{creditnote_id}/emailhistory`
- `/creditnotes/{creditnote_id}/address/billing`
- `/creditnotes/{creditnote_id}/address/shipping`
- `/creditnotes/templates`
- `/creditnotes/{creditnote_id}/templates/{template_id}`
- `/creditnotes/{creditnote_id}/invoices`
- `/creditnotes/{creditnote_id}/invoices/{creditnote_invoice_id}`
- `/creditnotes/{creditnote_id}/comments`
- `/creditnotes/{creditnote_id}/comments/{comment_id}`
- `/creditnotes/refunds`
- `/creditnotes/{creditnote_id}/refunds`
- `/creditnotes/{creditnote_id}/refunds/{creditnote_refund_id}`

## Currency (4)
File: `currency.yml`

Endpoints:
- `/settings/currencies`
- `/settings/currencies/{currency_id}`
- `/settings/currencies/{currency_id}/exchangerates`
- `/settings/currencies/{currency_id}/exchangerates/{exchange_rate_id}`

## Custom Modules (2)
File: `custom-modules.yml`

Endpoints:
- `/{module_name}`
- `/{module_name}/{module_id}`

## Customer Debit Notes (2)
File: `customer-debit-notes.yml`

Endpoints:
- `/invoices`
- `/invoices/{debit_note_id}`

## Customer Payments (5)
File: `customer-payments.yml`

Endpoints:
- `/customerpayments`
- `/customerpayments/{payment_id}`
- `/customerpayments/{customer_payment_id}/refunds`
- `/customerpayment/{customer_payment_id}/customfields`
- `/customerpayments/{customer_payment_id}/refunds/{refund_id}`

## Estimates (18)
File: `estimates.yml`

Endpoints:
- `/estimates`
- `/estimates/{estimate_id}`
- `/estimate/{estimate_id}/customfields`
- `/estimates/{estimate_id}/status/sent`
- `/estimates/{estimate_id}/status/accepted`
- `/estimates/{estimate_id}/status/declined`
- `/estimates/{estimate_id}/submit`
- `/estimates/{estimate_id}/approve`
- `/estimates/{estimate_id}/email`
- `/estimates/email`
- `/estimates/pdf`
- `/estimates/print`
- `/estimates/{estimate_id}/address/billing`
- `/estimates/{estimate_id}/address/shipping`
- `/estimates/templates`
- `/estimates/{estimate_id}/templates/{template_id}`
- `/estimates/{estimate_id}/comments`
- `/estimates/{estimate_id}/comments/{comment_id}`

## Expenses (8)
File: `expenses.yml`

Endpoints:
- `/expenses`
- `/expenses/{expense_id}`
- `/expenses/{expense_id}/comments`
- `/employees`
- `/employees/{employee_id}`
- `/employee/{employee_id}`
- `/expenses/{expense_id}/receipt`
- `/expenses/{expense_id}/attachment`

## Fixed Assets (13)
File: `fixed-assets.yml`

Endpoints:
- `/fixedassets`
- `/fixedassets/{fixed_asset_id}`
- `/fixedassets/{fixed_asset_id}/history`
- `/fixedassets/{fixed_asset_id}/forecast`
- `/fixedassets/{fixed_asset_id}/status/active`
- `/fixedassets/{fixed_asset_id}/status/cancel`
- `/fixedassets/{fixed_asset_id}/status/draft`
- `/fixedassets/{fixed_asset_id}/writeoff`
- `/fixedassets/{fixed_asset_id}/sell`
- `/fixedassets/{fixed_asset_id}/comments`
- `/fixedassets/{fixed_asset_id}/comments/{comment_id}`
- `/fixedassettypes`
- `/fixedassettypes/{fixed_asset_type_id}`

## ZOHO CRM Integration (4)
File: `integration.yml`

Endpoints:
- `/crm/account/{crm_account_id}/import`
- `/crm/contact/{crm_contact_id}/import`
- `/crm/vendor/{crm_vendor_id}/import`
- `/crm/item/{crm_product_id}/import`

## Invoices (35)
File: `invoices.yml`

Endpoints:
- `/invoices`
- `/invoices/{invoice_id}`
- `/invoices/{invoice_id}/status/sent`
- `/invoices/{invoice_id}/status/void`
- `/invoices/{invoice_id}/status/draft`
- `/invoices/email`
- `/invoices/fromsalesorder`
- `/invoices/mapwithorder`
- `/invoices/{invoice_id}/submit`
- `/invoices/{invoice_id}/approve`
- `/invoices/{invoice_id}/email`
- `/invoices/{invoice_id}/paymentreminder`
- `/invoices/paymentreminder`
- `/invoices/pdf`
- `/invoices/print`
- `/invoices/{invoice_id}/paymentreminder/disable`
- `/invoices/{invoice_id}/paymentreminder/enable`
- `/invoices/{invoice_id}/writeoff`
- `/invoices/{invoice_id}/writeoff/cancel`
- `/invoices/{invoice_id}/address/billing`
- `/invoices/{invoice_id}/address/shipping`
- `/invoices/templates`
- `/invoices/{invoice_id}/templates/{template_id}`
- `/invoices/{invoice_id}/payments`
- `/invoices/{invoice_id}/creditsapplied`
- `/invoices/{invoice_id}/credits`
- `/invoices/{invoice_id}/payments/{invoice_payment_id}`
- `/invoices/{invoice_id}/creditsapplied/{creditnotes_invoice_id}`
- `/invoices/{invoice_id}/attachment`
- `/invoices/{invoice_id}/documents/{document_id}`
- `/invoices/expenses/{expense_id}/receipt`
- `/invoice/{invoice_id}/customfields`
- `/invoices/{invoice_id}/comments`
- `/invoices/{invoice_id}/comments/{comment_id}`
- `/share/paymentlink`

## Items (6)
File: `items.yml`

Endpoints:
- `/items`
- `/itemdetails`
- `/items/{item_id}`
- `/item/{item_id}/customfields`
- `/items/{item_id}/active`
- `/items/{item_id}/inactive`

## Journals (6)
File: `journals.yml`

Endpoints:
- `/journals`
- `/journals/{journal_id}`
- `/journals/{journal_id}/status/publish`
- `/journals/{journal_id}/attachment`
- `/journals/{journal_id}/comments`
- `/journals/{journal_id}/comments/{comment_id}`

## Locations (6)
File: `locations.yml`

Endpoints:
- `/settings/locations/enable`
- `/locations`
- `/locations/{location_id}`
- `/locations/{location_id}/active`
- `/locations/{location_id}/inactive`
- `/locations/{location_id}/markasprimary`

## Opening Balance (1)
File: `opening-balance.yml`

Endpoints:
- `/settings/openingbalances`

## Organizations (2)
File: `organizations.yml`

Endpoints:
- `/organizations`
- `/organizations/{organization_id}`

## Projects (11)
File: `projects.yml`

Endpoints:
- `/projects`
- `/projects/{project_id}`
- `/projects/{project_id}/active`
- `/projects/{project_id}/inactive`
- `/projects/{project_id}/clone`
- `/projects/{project_id}/users`
- `/projects/{project_id}/users/invite`
- `/projects/{project_id}/users/{user_id}`
- `/projects/{project_id}/comments`
- `/projects/{project_id}/comments/{comment_id}`
- `/projects/{project_id}/invoices`

## Purchase Order (16)
File: `purchase-order.yml`

Endpoints:
- `/purchaseorders`
- `/purchaseorders/{purchase_order_id}`
- `/purchaseorder/{purchaseorder_id}/customfields`
- `/purchaseorders/{purchaseorder_id}/status/open`
- `/purchaseorders/{purchaseorder_id}/status/billed`
- `/purchaseorders/{purchaseorder_id}/status/cancelled`
- `/purchaseorders/{purchaseorder_id}/submit`
- `/purchaseorders/{purchaseorder_id}/approve`
- `/purchaseorders/{purchaseorder_id}/email`
- `/purchaseorders/{purchaseorder_id}/address/billing`
- `/purchaseorders/templates`
- `/purchaseorders/{purchaseorder_id}/templates/{template_id}`
- `/purchaseorders/{purchaseorder_id}/attachment`
- `/purchaseorders/{purchaseorder_id}/comments`
- `/purchaseorders/{purchaseorder_id}/comments/{comment_id}`
- `/purchaseorders/{purchaseorder_id}/reject`

## Recurring Bills (6)
File: `recurring-bills.yml`

Endpoints:
- `/recurringbills`
- `/recurringbills/{recurring_bill_id}`
- `/recurring_bills/{recurring_bill_id}`
- `/recurringbills/{recurring_bill_id}/status/stop`
- `/recurringbills/{recurring_bill_id}/status/resume`
- `/recurringbills/{recurring_bill_id}/comments`

## Recurring Expenses (6)
File: `recurring-expenses.yml`

Endpoints:
- `/recurringexpenses`
- `/recurringexpenses/{recurring_expense_id}`
- `/recurringexpenses/{recurring_expense_id}/status/stop`
- `/recurringexpenses/{recurring_expense_id}/status/resume`
- `/recurringexpenses/{recurring_expense_id}/expenses`
- `/recurringexpenses/{recurring_expense_id}/comments`

## Recurring Invoices (6)
File: `recurring-invoices.yml`

Endpoints:
- `/recurringinvoices`
- `/recurringinvoices/{recurring_invoice_id}`
- `/recurringinvoices/{recurring_invoice_id}/status/stop`
- `/recurringinvoices/{recurring_invoice_id}/status/resume`
- `/recurringinvoices/{recurring_invoice_id}/templates/{template_id}`
- `/recurringinvoices/{recurring_invoice_id}/comments`

## Reporting Tags (11)
File: `reporting-tags.yml`

Endpoints:
- `/reportingtags`
- `/reportingtags/{tag_id}`
- `/reportingtags/{tag_id}/options`
- `/reportingtags/{tag_id}/criteria`
- `/reportingtags/{tag_id}/active`
- `/reportingtags/{tag_id}/inactive`
- `/reportingtags/{tag_id}/option/(\d+)/active`
- `/reportingtags/{tag_id}/option/(\d+)/inactive`
- `/reportingtags/options`
- `/reportingtags/(\d+)/options/all`
- `/reportingtags/reorder`

## Retainer Invoices (15)
File: `retainer-invoices.yml`

Endpoints:
- `/retainerinvoices`
- `/retainerinvoices/{retainerinvoice_id}`
- `/retainerinvoices/{retainerinvoice_id}/status/sent`
- `/retainerinvoices/{retainerinvoice_id}/templates/{template_id}`
- `/retainerinvoices/{retainerinvoice_id}/status/void`
- `/retainerinvoices/{reatinerinvoice_id}/status/draft`
- `/retainerinvoices/{reatinerinvoice_id}/submit`
- `/retainerinvoices/{reatinerinvoice_id}/approve`
- `/retainerinvoices/{retainerinvoice_id}/email`
- `/retainerinvoices/{retainerinvoice_id}/address/billing`
- `/retainerinvoices/templates`
- `/retainerinvoices/{retainerinvoice_id}/attachment`
- `/retainerinvoices/{retainerinvoice_id}/documents/{document_id}`
- `/retainerinvoices/{retainerinvoice_id}/comments`
- `/retainerinvoices/{retainerinvoice_id}/comments/{comment_id}`

## Sales Order (18)
File: `sales-order.yml`

Endpoints:
- `/salesorders`
- `/salesorders/{salesorder_id}`
- `/salesorder/{salesorder_id}/customfields`
- `/salesorders/{salesorder_id}/status/open`
- `/salesorders/{salesorder_id}/status/void`
- `/salesorders/{salesorder_id}/substatus/{status_code}`
- `/salesorders/{salesorder_id}/email`
- `/salesorders/{salesorder_id}/submit`
- `/salesorders/{salesorder_id}/approve`
- `/salesorders/pdf`
- `/salesorders/print`
- `/salesorders/{salesorder_id}/address/billing`
- `/salesorders/{salesorder_id}/address/shipping`
- `/salesorders/templates`
- `/salesorders/{salesorder_id}/templates/{template_id}`
- `/salesorders/{salesorder_id}/attachment`
- `/salesorders/{salesorder_id}/comments`
- `/salesorders/{salesorder_id}/comments/{comment_id}`

## Sales Receipt (3)
File: `sales-receipt.yml`

Endpoints:
- `/salesreceipts`
- `/salesreceipts/{sales_receipt_id}`
- `/salesreceipts/{sales_receipt_id}/email`

## Tasks (2)
File: `tasks.yml`

Endpoints:
- `/projects/{project_id}/tasks`
- `/projects/{project_id}/tasks/{task_id}`

## Taxes (8)
File: `taxes.yml`

Endpoints:
- `/settings/taxes`
- `/settings/taxes/{tax_id}`
- `/settings/taxgroups/{tax_group_id}`
- `/settings/taxgroups`
- `/settings/taxauthorities`
- `/settings/taxauthorities/{tax_authority_id}`
- `/settings/taxexemptions`
- `/settings/taxexemptions/{tax_exemption_id}`

## Time Entries (5)
File: `time-entries.yml`

Endpoints:
- `/projects/timeentries`
- `/projects/timeentries/{time_entry_id}`
- `/projects/timeentries/{time_entry_id}/timer/start`
- `/projects/timeentries/timer/stop`
- `/projects/timeentries/runningtimer/me`

## Users (6)
File: `users.yml`

Endpoints:
- `/users`
- `/users/{user_id}`
- `/users/me`
- `/users/{user_id}/invite`
- `/users/{user_id}/active`
- `/users/{user_id}/inactive`

## Vendor Credits (13)
File: `vendor-credits.yml`

Endpoints:
- `/vendorcredits`
- `/vendorcredits/{vendor_credit_id}`
- `/vendorcredits/{vendor_credit_id}/status/open`
- `/vendorcredits/{vendor_credit_id}/status/void`
- `/vendorcredits/{vendor_credit_id}/submit`
- `/vendorcredits/{vendor_credit_id}/approve`
- `/vendorcredits/{vendor_credit_id}/bills`
- `/vendorcredits/{vendor_credit_id}/bills/{vendor_credit_bill_id}`
- `/vendorcredits/{vendor_credit_id}/refunds`
- `/vendorcredits/{vendor_credit_id}/refunds/{vendor_credit_refund_id}`
- `/vendorcredits/refunds`
- `/vendorcredits/{vendor_credit_id}/comments`
- `/vendorcredits/{vendor_credit_id}/comments/{comment_id}`

## Vendor Payments (5)
File: `vendor-payments.yml`

Endpoints:
- `/vendorpayments`
- `/vendorpayments/{payment_id}`
- `/vendorpayments/{payment_id}/refunds`
- `/vendorpayments/{payment_id}/refunds/{vendorpayment_refund_id}`
- `/vendorpayments/{payment_id}/email`

