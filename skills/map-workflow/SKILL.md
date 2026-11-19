---
name: map-workflow
description: Map a business workflow as it is done today, step by step, from interviews, notes, transcripts, SOPs or screenshots. Use before automating anything, or when someone asks to map, document or understand a process.
---

# Map a workflow

Produce a step-level map of one workflow as people actually do it today. The map is the input for find-automation-candidates. Nothing gets automated until the map is agreed with the people who do the work.

## Inputs

- What the user gives: interview notes or transcripts, emails, SOPs, screenshots of the tools, or a spoken description.
- Ask for anything missing in step 1. Do not guess volumes or times.

## Steps

1. **Set the boundary.** Write down, in one line each:
   - Trigger: what starts the workflow (an email arrives, a form is submitted, a date passes).
   - End result: what exists when it is done, and for whom.
   - Owner: the role accountable for the result.
   - Volume: how often it runs per week or month.
   If any of these is unknown, ask before going on.

2. **List the steps in order.** One action per step, written as role + verb + object ("Accounts clerk checks the invoice against the purchase order"). For each step record:
   - Role (not a person's name)
   - Tool or system used, by its real name
   - Input and output
   - Time per occurrence (hands-on minutes)
   - Wait before the next step
   - How often it needs rework, if known
   Write `to ask` in any cell nobody has confirmed. Never fill a cell with an estimate without marking it `estimate`.

3. **Mark the friction.** Flag every step that is:
   - a handoff between roles or teams
   - a wait or queue
   - a rework loop
   - an approval
   - manual re-entry of data that already exists in another system
   - copy and paste between tools

4. **Describe practice, not policy.** If the SOP and the interviews disagree, map what people do and note the difference.

5. **Check the map with the people who do the work.** Record who confirmed it and on which date. Keep their corrections.

## Output

Save `workflow-map.md` with:

- The boundary block from step 1.
- The step table from step 2, with the friction flags as a column.
- A Mermaid flowchart with one subgraph per role, so handoffs are visible.
- Open questions, each with the person who can answer it.
- Totals: hands-on hours per month (time per occurrence × volume, summed), with the arithmetic shown.

## Rules

- Plain language. Name the actual tool, not "the system".
- No recommendations in the map. Those come in the next skill.
- If the workflow has more than about 25 steps, split it into sub-workflows and map each one.
