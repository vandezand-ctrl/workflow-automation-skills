---
name: automation-business-case
description: Turn the top automation candidates into a one-page business case with hours saved, cost, risk, payback and the decision asked for. Use after find-automation-candidates, when someone has to approve time or budget.
---

# Automation business case

A decision-maker needs one page: what changes, what it saves, what it costs, what could go wrong, and what they are asked to approve.

## Inputs

- `automation-candidates.md` (from find-automation-candidates).
- From the user: loaded hourly cost per role, build effort or quotes, tool licences, and who decides. Ask for each; never assume a salary or a price.

## Steps

1. **Per candidate, set out:**
   - Hours saved per month, from the candidates file, with its assumptions.
   - Value per year: hours saved × 12 × loaded hourly cost of the role.
   - One-off cost: build hours × rate, plus set-up and training.
   - Running cost per year: licences, AI usage, maintenance hours.
   - Payback in months: one-off cost ÷ (monthly value − monthly running cost).
   - Other effects that matter but are not counted: faster lead time, fewer errors, better data. State them; do not convert them into money unless the user gives a basis.

2. **Show the sensitivity.** Recompute payback with the share of work removed at half the assumed level. If the case only works at the assumed level, say so.

3. **Name the risks** with one control each: wrong outputs, adoption, data access, dependence on one person.

4. **State the decision asked for:** what is approved, by whom, and the review date when the pilot result is checked.

## Output

`business-case.md`: one page with a table per candidate, the sensitivity line, the risks and the decision. All arithmetic shown.

## Rules

- Savings are capacity, not cash, unless the user says the time will be cut or redeployed. Write which one it is.
- Every figure is either from the user, from the candidates file, or marked as an assumption.
