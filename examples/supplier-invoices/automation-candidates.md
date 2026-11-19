# Example: automation candidates (fictional)

Output of find-automation-candidates for the fictional workflow in `workflow-map.md`. Shares of work removed are assumptions until a pilot measures them.

| Step | Route | Hours saved a month | Risk | Effort | Preconditions |
|---|---|---|---|---|---|
| 3 Type invoice into ERP | AI with human approval: AI extracts header and lines, clerk checks and posts | 7,200 × 70% ÷ 60 = 84 | Medium: wrong amounts | Medium | Share of scanned images known; test set of 50 past invoices |
| 4 Match to PO and receipt | Rule-based three-way match in the ERP | 4,800 × 85% ÷ 60 = 68 | Low: mismatches go to the clerk | Low | Goods receipts recorded on delivery day |
| 2 Save PDF to drive | Rule-based: inbox rule files attachments by supplier | 2,400 × 100% ÷ 60 = 40 | Low | Low | One inbox for all invoices |
| 7 Schedule payment | Rule-based: twice-weekly batch payment file from the ERP | 1,200 × 90% ÷ 60 = 18 | Medium: payment errors | Medium | Bank accepts batch files; approval stays with finance |
| 5 Mismatch emails | Simplify first: buyer answers in the ERP, not by email; AI drafts the query with the differences listed | 180 × 4 × 50% ÷ 60 = 6 | Low | Low | Buyers have ERP access |
| 6 Approval above EUR 5,000 | Keep manual, route through the ERP approval workflow | 0 | High if removed | Low | None |

## Top three

1. **AI extraction with clerk approval (step 3).** Saves about 84 hours a month. First: count scanned images and build a test set of 50 past invoices. Approver: AP clerk, with the AP lead reviewing the error log weekly.
2. **Three-way match in the ERP (step 4).** Saves about 68 hours a month. First: goods receipts recorded on delivery day. Approver for exceptions: AP clerk.
3. **Inbox rule for attachments (step 2).** Saves about 40 hours a month. First: one inbox for all supplier invoices. No approval needed.

Together about 192 of the 295 hands-on hours a month, before the pilot measures the real shares.
