# Evaluation report

- Cases in the evaluation set: 20
- Cases without an output: 0
- Cases with every field correct: 16 of 20 (80%)
- Required: 90%. Result: FAIL

## Accuracy per field

| Field | Correct | Accuracy |
|---|---:|---:|
| supplier | 19 of 20 | 95% |
| invoice_number | 20 of 20 | 100% |
| invoice_date | 20 of 20 | 100% |
| total_amount | 19 of 20 | 95% |
| currency | 19 of 20 | 95% |
| po_number | 19 of 20 | 95% |

## Mismatches

| Case | Field | Expected | Got |
|---|---|---|---|
| EV-03 | total_amount | 1630.79 | 16307.9 |
| EV-11 | po_number | PO-40378 |  |
| EV-14 | supplier | Linden Paper Co | Delta Office |
| EV-18 | currency | EUR | USD |
