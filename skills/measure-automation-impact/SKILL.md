---
name: measure-automation-impact
description: Measure an automation's result against the baseline from the workflow map and write a one-page impact report with what was saved, what changed in quality and lead time, and what to do next. Use at the review date after rollout.
---

# Measure automation impact

The business case promised a result. This skill checks it with the same measures, so the next decision rests on facts.

## Inputs

- The baseline: `workflow-map.md` (hands-on hours per month), `process-log-analysis.md` (lead times), and the error or rework rate from before.
- The same measures after rollout: a new process log export, a time sample or user reports, and the adoption tracking from rollout-and-adoption.

## Steps

1. **Use the same definitions** as the baseline. If a measure changed definition, say so and do not compare it.
2. **Compare:**
   - hands-on hours per month
   - median and 90th percentile lead time
   - error or rework rate
   - share of cases through the new route
3. **Explain the gaps** between the business case and the result: adoption, fallbacks, volume changes, a wrong assumption.
4. **Recommend one of three:** keep as is, improve (with the specific change), or stop.

## Output

`impact-report.md`: one page with a before-and-after table, the gaps explained, and the recommendation. All arithmetic shown.

## Rules

- Report the result even when it is below the business case.
- Count time saved only once: if a step became faster and also less frequent, do not add both.
