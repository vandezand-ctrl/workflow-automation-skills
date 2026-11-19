---
name: build-eval-set
description: Build an evaluation set of real past cases with checked expected outputs for every AI step in an automation, and score the AI's outputs against it with a script. Use before rollout and after every change to a prompt, model or input.
---

# Build an evaluation set

An AI step is only as reliable as the evidence behind it. An evaluation set is that evidence: real cases, the right answers, and a score that is rerun after every change.

## Steps

1. **Collect cases.** At least 20 real past cases per AI step, chosen to include the awkward ones: poor scans, unusual layouts, missing fields, edge amounts, other languages. Remove personal data the evaluation does not need.

2. **Write the expected output** for each case, checked by the person who does the work today. One column per field the AI must produce. Save as `expected.csv` with an `id` column.

3. **Run the AI step** on the same cases and save its output as `actual.csv` with the same columns.

4. **Score it:**

   ```
   python scripts/run_evals.py expected.csv actual.csv --numeric total_amount --min-pass 0.9 --out eval-report.md
   ```

   Text fields are compared after trimming and lower-casing; `--numeric` fields within `--tolerance`. The script exits with code 1 below `--min-pass`, so it can block a change in a pipeline. It uses the Python standard library only.

5. **Decide with the owner:**
   - The pass rate required before rollout, per field if some fields matter more.
   - Which errors the approval step will catch and which it will not.
   - Whether to fix the prompt, the input, or the process before trying again.

6. **Keep the set alive.** Add every wrong output found in production as a new case.

## Output

`expected.csv`, `actual.csv`, `eval-report.md`, and a line in the automation specification with the agreed pass rate.

## Rules

- No rollout of an AI step without a scored evaluation set.
- Rerun the evaluation after every change to a prompt, a model or the input format.
