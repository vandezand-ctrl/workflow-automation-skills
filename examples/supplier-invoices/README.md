# Worked example: supplier invoice processing (fictional)

Example Co. is a fictional 300-person distributor. The company, people, suppliers and all figures are invented to show what the skills produce. The process log is generated sample data.

| Stage | Skill | File |
|---|---|---|
| Discover | map-workflow | [workflow-map.md](workflow-map.md) |
| Discover | analyse-process-log | [process-log.csv](process-log.csv) (input: a sample of 300 invoices exported for September), [process-log-analysis.md](process-log-analysis.md) (script output) |
| Decide | find-automation-candidates | [automation-candidates.md](automation-candidates.md) |
| Decide | automation-business-case | [business-case.md](business-case.md) |
| Test | build-eval-set | [evals/expected.csv](evals/expected.csv), [evals/actual.csv](evals/actual.csv), [evals/eval-report.md](evals/eval-report.md) (script output: 80% against a 90% target, so the AI extraction is not ready for rollout) |

Reproduce the two script outputs:

```
python ../../skills/analyse-process-log/scripts/analyse_process_log.py process-log.csv --out process-log-analysis.md
python ../../skills/build-eval-set/scripts/run_evals.py evals/expected.csv evals/actual.csv --numeric total_amount --min-pass 0.9 --out evals/eval-report.md
```
