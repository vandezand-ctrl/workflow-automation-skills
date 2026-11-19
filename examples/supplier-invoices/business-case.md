# Example: business case (fictional)

Output of automation-business-case for the fictional Example Co. Hourly cost, build effort and prices are invented for illustration.

Assumptions given by the (fictional) user: loaded cost of an AP clerk EUR 30 an hour; build and configuration work EUR 60 an hour. Savings are capacity: the AP lead plans to move the freed time to supplier onboarding, not to cut staff.

| | AI extraction with clerk approval (step 3) | Three-way match in the ERP (step 4) | Inbox rule for attachments (step 2) |
|---|---:|---:|---:|
| Hours saved per month | 84 | 68 | 40 |
| Value per year | 84 × 12 × 30 = EUR 30,240 | 68 × 12 × 30 = EUR 24,480 | 40 × 12 × 30 = EUR 14,400 |
| One-off cost | 80 h × 60 + 1,000 set-up = EUR 5,800 | 24 h × 60 + 500 training = EUR 1,940 | 4 h × 60 = EUR 240 |
| Running cost per year | AI usage 1,200 + 4 h a month maintenance 2,880 = EUR 4,080 | 1 h a month × 60 × 12 = EUR 720 | none |
| Payback | 5,800 ÷ (2,520 − 340) = 2.7 months | 1,940 ÷ (2,040 − 60) = 1.0 month | 240 ÷ 1,200 = 0.2 months |
| Payback if only half the work is removed | 5,800 ÷ (1,260 − 340) = 6.3 months | 1,940 ÷ (1,020 − 60) = 2.0 months | 240 ÷ 600 = 0.4 months |

Not counted in money: the median invoice takes 4.9 days from receipt to payment scheduling (process log), and 20% of invoices are matched twice because of buyer queries. Both should fall, which reduces late-payment disputes.

## Risks and controls

- **Wrong amounts from AI extraction.** The clerk approves every extracted invoice; the evaluation set must reach 90% fully correct before rollout (it is at 80% now, see `evals/eval-report.md`).
- **Goods receipts recorded late,** which breaks the three-way match. The warehouse lead commits to same-day receipts before the match goes live.
- **Adoption.** The shared-drive route is switched off on a fixed date (rollout plan).

## Decision asked

The finance director approves EUR 7,980 one-off and EUR 4,800 a year running cost for the three changes, with a pilot in one entity and a review of the impact report after three months.
