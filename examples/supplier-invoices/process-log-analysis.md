# Process log analysis

- Cases: 300
- Events: 1767
- Period: 2026-09-01 to 2026-10-09
- Throughput time per case: median 4.9 days, 90th percentile 10.0 days

## Steps

| Activity | Events | Cases | Share of cases | Median wait before | 90th percentile wait |
|---|---:|---:|---:|---:|---:|
| Invoice received | 300 | 300 | 100% | start |  |
| Saved to shared drive | 300 | 300 | 100% | 23.7 h | 29.8 h |
| Entered in ERP | 300 | 300 | 100% | 18.7 h | 24.6 h |
| Matched to PO and receipt | 360 | 300 | 100% | 4.5 h | 16.8 h |
| Payment scheduled | 300 | 300 | 100% | 42.1 h | 3.7 days |
| Query sent to buyer | 78 | 60 | 20% | 2.8 h | 16.0 h |
| Buyer replied | 78 | 60 | 20% | 3.7 days | 5.7 days |
| Approved by finance | 51 | 51 | 17% | 2.6 days | 4.0 days |

## Slowest handoffs

Transitions with at least 5 occurrences, ordered by median wait.

| From | To | Times | Median wait | Total wait |
|---|---|---:|---:|---:|
| Query sent to buyer | Buyer replied | 78 | 3.7 days | 276.7 days |
| Matched to PO and receipt | Approved by finance | 51 | 2.6 days | 131.6 days |
| Approved by finance | Payment scheduled | 51 | 47.3 h | 99.4 days |
| Matched to PO and receipt | Payment scheduled | 249 | 41.8 h | 468.6 days |
| Invoice received | Saved to shared drive | 300 | 23.7 h | 293.7 days |

## Rework

| Activity repeated within a case | Cases | Share of cases |
|---|---:|---:|
| Matched to PO and receipt | 60 | 20% |
| Query sent to buyer | 18 | 6% |
| Buyer replied | 18 | 6% |

## Most common paths

| Path | Cases | Share |
|---|---:|---:|
| Invoice received > Saved to shared drive > Entered in ERP > Matched to PO and receipt > Payment scheduled | 203 | 68% |
| Invoice received > Saved to shared drive > Entered in ERP > Matched to PO and receipt > Approved by finance > Payment scheduled | 37 | 12% |
| Invoice received > Saved to shared drive > Entered in ERP > Matched to PO and receipt > Query sent to buyer > Buyer replied > Matched to PO and receipt > Payment scheduled | 33 | 11% |
| Invoice received > Saved to shared drive > Entered in ERP > Matched to PO and receipt > Query sent to buyer > Buyer replied > Query sent to buyer > Buyer replied > Matched to PO and receipt > Payment scheduled | 13 | 4% |
| Invoice received > Saved to shared drive > Entered in ERP > Matched to PO and receipt > Query sent to buyer > Buyer replied > Matched to PO and receipt > Approved by finance > Payment scheduled | 9 | 3% |

6 distinct paths in total.
