---
name: design-automation
description: Turn one automation candidate into a buildable specification with trigger, data, the AI's role, the human approval step, controls, test cases, success measures and a rollout plan. Use after find-automation-candidates, before anyone builds.
---

# Design an automation

Take one candidate from `automation-candidates.md` and write the specification a builder (a person or an AI coding tool) can work from without guessing.

## Steps

1. **Trigger and scope.** What starts it, what it covers, what it explicitly does not cover.

2. **Data.** Every input with its source system, owner and access right. Every output with where it is stored. Flag personal or confidential data and where it may and may not go.

3. **Flow.** The new steps in order, in the same table format as the workflow map, so old and new can be compared line by line.

4. **The AI's role and the person's role.** For each AI step: what the AI reads, what it drafts or decides, and which named role approves, edits or rejects it. Nothing the AI drafts reaches a customer, a payment or a record of truth without that approval, unless the user decides otherwise in writing.

5. **Controls.**
   - Audit log: who approved what, when, with the AI's draft kept next to the final version.
   - Fallback: what happens when the AI is unsure, the input is unreadable or a tool is down. The work goes back to the manual route; it never stops silently.
   - Access by role.
   - A way for users to report a wrong output, and who reviews those reports.

6. **Test cases.** At least ten real past cases, including the awkward ones, with the expected output for each. For AI steps, keep these as an evaluation set and rerun them after every change to prompts or models.

7. **Success measures.** The baseline from the workflow map and the target after rollout: hands-on hours per month, lead time from trigger to end result, error or rework rate, and user adoption.

8. **Rollout.** Pilot group and length, training, the owner after go-live, the date the old route is switched off, and the review date where the measures are checked.

## Output

Save `automation-spec.md` with the eight sections above. End with a short build plan: components, order of work, and what to demo for approval before full build.

## Rules

- One automation per specification.
- Every figure either comes from the workflow map or is marked as an assumption.
- If a control cannot be met, say so in the specification instead of dropping it.
