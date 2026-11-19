---
name: process-discovery-interview
description: Prepare and run discovery interviews with the people who do a process, and turn the answers into structured notes that map-workflow can use. Use at the start of any process improvement or automation project.
---

# Process discovery interview

The people who do the work know the process better than any SOP. This skill prepares the interviews, keeps them on facts, and turns the answers into notes in one fixed shape.

## Steps

1. **Plan who to talk to.** One person per role in the process, plus whoever owns the result. Two people for the role that handles most of the volume, because they often work differently. Ask the user for names and roles; do not guess them.

2. **Write the guide.** Thirty minutes per interview. Questions ask about the last time something happened, not about how it usually goes:
   - "Walk me through the last invoice you handled, from the moment it arrived."
   - "Which screens or files did you have open?"
   - "Where did you wait for someone else? How long?"
   - "When did you last have to redo something? Why?"
   - "What do you copy from one place to another?"
   - "What would you stop doing tomorrow if you could?"
   Add role-specific questions from what the user already knows about the process.

3. **During or after the interview, take notes in this shape:**
   - Role and date
   - Steps in their words, in order, with the tool used
   - Times and volumes they gave (with "their estimate" where it is one)
   - Waits, handoffs, rework, workarounds
   - Exceptions and how often they happen
   - Ideas they mentioned
   - Open questions

4. **Compare across interviews.** List where people describe the same step differently. These differences are findings, not errors: they often point to the real cause of delay.

## Output

- `interview-guide.md` with the plan and the questions per role.
- One `interview-<role>-<date>.md` per interview, in the shape of step 3.
- `interview-findings.md`: differences between interviews and open questions, ready for map-workflow.

## Rules

- Ask about specific recent cases. "Usually" answers hide the exceptions that cost the most time.
- Do not suggest solutions in the interview.
- Record times as given and mark them as estimates; the process log or a time sample can confirm them later.
