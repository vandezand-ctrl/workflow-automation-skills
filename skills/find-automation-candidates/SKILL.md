---
name: find-automation-candidates
description: Score each step of a mapped workflow and rank where to remove, simplify, automate with rules, automate with AI plus a human approval, or build software. Use after map-workflow, or when someone asks what to automate first.
---

# Find automation candidates

Work from an agreed `workflow-map.md`. If there is none, run map-workflow first.

## Steps

1. **Score every step** on six questions. Use the map's figures; mark anything assumed.
   - Volume: how often does it run?
   - Time: hands-on minutes per occurrence?
   - Rules or judgement: can the decision be written as rules, or does it need judgement?
   - Input: structured (fields, tables), semi-structured (forms, invoices) or unstructured (emails, notes, calls)?
   - Cost of an error: what happens if this step goes wrong, and who notices?
   - Data access: can a tool read the inputs today, and is it allowed to?

2. **Classify every step into one route:**
   - **Remove:** the step adds nothing anyone uses.
   - **Simplify or standardize:** fix the step itself first (one template, one owner, one place to store it).
   - **Rule-based automation:** structured inputs and clear rules; no-code tools (Zapier, Make, Power Automate, Apps Script) or a script.
   - **AI with human approval:** semi-structured or unstructured inputs, or a draft that needs judgement. AI prepares, a named person approves.
   - **Software:** several steps share the same data, roles and status, so a small application is cheaper than linking tools.
   - **Keep manual:** low volume, high judgement, or high cost of error with no safe check.

3. **Estimate the saving per candidate.** Hours per month = volume × hands-on minutes × share of the work removed ÷ 60. Show the arithmetic. Mark the share removed as an assumption until a pilot measures it.

4. **Check what must be true first.** Automation copies a broken process faster. For each candidate list the preconditions: data quality, an agreed process, an owner, access rights. A candidate whose preconditions are not met goes to "Simplify or standardize" first.

5. **Rank.** Order by hours saved, then by risk (cost of an error, data sensitivity), then by effort.

## Output

Save `automation-candidates.md` with:

- A table: step, route, hours saved per month, risk, effort, preconditions.
- The top three candidates, each in four lines: what changes, what it saves, what must be true first, who approves.
- Steps classified "Remove" or "Simplify", listed separately; these often save more than automation does.

## Rules

- No candidate without a figure or a stated assumption behind it.
- Do not recommend AI where a rule does the job.
- Every AI route names the person who approves the output.
