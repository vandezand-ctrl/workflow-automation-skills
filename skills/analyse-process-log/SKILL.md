---
name: analyse-process-log
description: Analyse an event log exported from a ticketing, CRM, ERP or workflow system to find throughput times, waits per step, the slowest handoffs, rework and the most common paths. Use when a system can export case history, to check the interviews with data.
---

# Analyse a process log

Interviews say how people experience a process. The system's history shows what actually happened. This skill reads an export and reports where time goes.

## Inputs

A CSV with one row per event and at least three columns:

- a case id (invoice number, ticket number, order number)
- an activity name (status or step)
- a timestamp

Most systems can export this from a status history, audit log or activity table. If the user has a database instead of an export, write the SQL that produces these three columns and ask the user to run it.

## Steps

1. **Check the export.** Count rows, cases and activities. Look for missing timestamps, activities with near-identical names ("Approved" and "approved by finance") and cases that never finish. Ask the user how to treat them before analysing.

2. **Run the script:**

   ```
   python scripts/analyse_process_log.py process-log.csv --out process-log-analysis.md
   ```

   Use `--case`, `--activity` and `--timestamp` when the columns have other names. The script uses the Python standard library only.

3. **Read the report with the user.** It shows:
   - throughput time per case (median and 90th percentile)
   - per step: how many cases pass through it and the wait before it
   - the slowest handoffs between two steps
   - rework: steps repeated within one case
   - the most common paths through the process

4. **Compare with the workflow map.** Note where the data confirms the interviews and where it does not. Waits usually explain more of the throughput time than hands-on work does.

## Output

`process-log-analysis.md` from the script, plus a short `process-log-findings.md` with three to five findings, each with the figure behind it and the step in the workflow map it belongs to.

## Rules

- The log shows waits between recorded events, not hands-on time. Do not present waits as effort.
- Never send a log with personal data to a tool the organisation has not approved. Replace names with roles before analysis if needed.
