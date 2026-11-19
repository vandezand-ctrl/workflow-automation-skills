---
name: review-plan
description: CTO-level review of an implementation plan, runs six mandatory evidence sweeps, then only the judgement dimensions the plan's files actually reach, and records a sweep ledger in the plan so successive passes converge instead of finding fresh criticals forever
argument-hint: [path-to-plan.md]
allowed-tools: Read, Glob, Grep, Bash, AskUserQuestion, Edit
user-invocable: true
---

Review an implementation plan the way a CTO who has been burned would: **verify first, judge second.**

## Why this skill is shaped this way, read this once

On 2026-08-31 the previous version of this skill ran four passes over one small plan and produced
criticals on every pass, including the fourth. The plan owner's verdict: *"It is not acceptable that after 4
reviews, we are still finding 2 critical issues."* He was right, and the post-mortem is the design
brief.

Twelve findings came out of those four passes. **Eleven came from four deterministic sweeps** , 
reading the tooling the plan would run into, auditing the plan against the task's own acceptance
list, grepping for other places stating the same rule, and reading the target file's own conventions.
**One came from design judgement.** The old version required none of the four and explicitly said
*"do not do exhaustive codebase analysis"*, so every pass found whatever it happened to open. Pass 1
could have found the pass-4 items and the reverse; the ordering was luck, and luck does not converge.

**So the sweeps are mandatory, they go first, and the review declares which it ran.** A pass that
skips one says so, instead of leaving the next pass to discover an unexamined category.

## Step 1: Locate the plan

If `$ARGUMENTS` names a file, use it.

Otherwise glob **both** `.claude/plans/*.md` in the working directory **and** `~/.claude/plans/*.md`,
merging the results and **de-duplicating by absolute path** in case the two globs overlap. Plan-mode
plans are written to the user directory, not the project, and looking in only one place is how a
review gets run against the wrong file, or reports no plans when one exists. One match: use it.
Several: offer the five most recently modified via `AskUserQuestion`. None in either location: say so
and stop.

Read it fully. Keep the path, you will edit this file.

**Then read any `## Review Notes` at the bottom.** If they exist, this is pass N: read every previous
pass's Sweep Ledger and Applied Changes before doing anything else. Step 6 cannot work without them.

## Step 2: Establish the ground truth the plan is judged against

Not "gather context", **find the authorities.** In this order:

1. **The task's own acceptance criteria.** The `Done When`, `Acceptance`, `Requirements` or `Success`
   list in the bead, ticket, PRD or issue the plan implements. Read it verbatim. **This is the
   contract; the plan is only a proposal about how to meet it.** If the plan does not name its task,
   ask which one it implements.
2. **The project's operating rules.** `CLAUDE.md`, `AGENT.md` / `AGENTS.md`, `CONTRIBUTING.md`,
   `OPERATING-CONSTRAINTS.md` or equivalent. Note the hard prohibitions and any file the project
   treats specially.
3. **What the plan actually touches.** List the files. This routes Step 4.
4. **Whether the tree still matches the plan.** `git log --oneline -15` and `git status -sb`. A plan
   written against a tree that has since moved is reviewing fiction.

**Do not skip 1.** Three of the twelve findings in the worked example were *"the plan under-delivers a
stated requirement"*, and nothing but reading the list catches those.

## Step 3: The six mandatory sweeps

Run all six before forming any opinion. Each produces one ledger line naming what you checked and
what you found, **including "nothing"**. Never flag what you have not verified in the source; never
skip a sweep silently.

### Sweep 1, Requirement audit
Walk the acceptance list from Step 2 **one item at a time** and mark each `covered`, `partial` or
`absent` against the plan. Quote the item. **A `partial` is a finding**: name the half that is
missing.

> *Worked example:* an item read *"X, and the transitions do the same"*. The plan carried the first
> clause only. One clause, and no amount of general reading would have surfaced it.

### Sweep 2, Gate reading
**Find every gate that can refuse this work and read its code, not its documentation.** Test runners,
pre-commit hooks, CI, validators, schema checks, close or merge gates, permission checks. For each:
what exactly does it require, and does the plan satisfy it?

> *Worked example:* two blockers. The plan's step list omitted a mandatory transition and would have
> been refused outright. And a closeout field is parsed **only up to its first clause**, so a truthful
> write-up naming unfixed findings would have blocked the close. Both were one grep away, and neither
> was stated in any document.

### Sweep 3, Claim verification
**List every factual claim the plan makes about how something behaves, and check each against the
source.** Especially claims inherited from the task description, **a plan that faithfully repeats its
ticket is not thereby correct.**

> *Worked example:* the task asked the plan to state that a tool proves a hand resolution correct. The
> tool never writes the section in question, so both sides of its comparison are identical by
> construction and it proves nothing about it. Writing the requirement as given would have added a
> fresh false sentence to the very document being fixed.

### Sweep 4, Duplicate-statement sweep
**Grep for every other place that states what this plan changes**, the same rule, string, constant,
threshold, message or behaviour. Then ask: **after this change, do any two of them disagree?**

> *Worked example:* the single largest finding of all four passes. Two rule documents gave opposite
> instructions on the same command afterwards, and nothing in the repository ranked them. Cost: one
> grep for the changed sentence. **This sweep is the cheapest and the most often skipped.**

### Sweep 5, Target-file conventions
**Read the file being changed, in full, around the change.** What conventions does it keep on itself , 
a dated header stack, a changelog line, an ordering rule, a "this table must not be updated" note?
Does the plan honour them? And **what live content sits inside the block being replaced?**

> *Worked example:* two findings, a required dated header entry the plan omitted, and four unrelated
> live rules sitting inside the paragraph being rewritten, which a careless replace would have
> silently deleted.

### Sweep 6, Freshness and collision
`git fetch --prune`, then check whether the plan's premises still hold. Has the target moved? Is
another branch, worktree or session working the same files? Does the plan's sequencing survive someone
else's commit landing mid-build?

> *Worked example:* three separate incidents in one day in a shared checkout, one of which landed
> another session's commit on the branch under review.

## Step 4: Routed judgement dimensions

**Load `review-criteria.md` and apply only the dimensions the plan's file list actually reaches.** That
file states which kinds of files trigger which dimension.

A documentation change does not get a SQL-injection review. Running all eight dimensions on every plan
is what made the old output read as boilerplate, and boilerplate is what a reader learns to skim.

**If no dimension is triggered, say so in one line.** That is a legitimate result, not a gap.

## Step 5: Present the verdict

```
## Plan Review: <plan name>, pass N

### Sweep Ledger
| Sweep | Checked | Result |
|---|---|---|
| 1 Requirement audit | 6 Done When items | 3 covered, 2 partial, 1 absent |
| 2 Gate reading | close gate, pre-commit hook, checkpoint validator | 2 blockers |
| 3 Claim verification | 4 claims about tool behaviour | 1 false |
| 4 Duplicate statements | grep "<the changed string>" | 2 other locations, 1 conflicts |
| 5 Target conventions | header stack, replaced block | 2 findings |
| 6 Freshness | fetch, branches, worktrees | clean |

### Dimensions applied
<which, and one line on why the others were not>

### Executive Summary
<2-3 sentences: assessment, biggest concern, and on pass 2+ the MISS / NEW SCOPE split>

### Verdict: APPROVE / REVISE / CONVERGED
```

Then findings, most severe first:

```
N. **<title>** (<sweep or dimension>, *<exact heading of the plan section to fix>*)
   <2-4 sentences: the defect, why it matters, the risk, with the file:line that proves it>
   **Recommendation:** <the specific change to make in the plan>
```

**Section** must be a heading copied character-for-character out of the plan, or
`NEW (after: <exact heading>)`. A heading that does not appear verbatim cannot be located in Step 8.
Two sections needing changes is two findings.

Omit severity groups with no findings. End with `**Summary:** N critical, N warning, N suggestion`.

**Verdict rules:**

- **REVISE**, any CRITICAL.
- **APPROVE**, no CRITICAL.
- **CONVERGED**, no CRITICAL **and** no MISS. Say it plainly: *"All six sweeps ran clean. Further
  passes are unlikely to find structural issues."* **Then stop offering more passes.** Volunteering a
  fifth pass on a converged plan wastes the user's time and trains them to distrust the verdict.

## Step 6: On pass 2 and later, classify every finding

This is what makes passes converge, and its absence is what produced the complaint.

Label each finding on any pass after the first:

- **MISS**, it was true and findable at the earlier pass. **Name the sweep that would have caught
  it.** If no sweep would have, that is a gap in *this skill*: say so, and propose the sweep that
  closes it.
- **NEW SCOPE**, it is a consequence of a decision taken *after* that pass, usually the user's. **Not
  a review failure, and it must not be counted as one.**

State the split in the Executive Summary, *"Two criticals: both NEW SCOPE, from your decision to add
X. Nothing was missed."* **A pass whose findings are all NEW SCOPE has converged.**

> *Worked example:* pass 4's two criticals were both consequences of a scope decision the user took at
> pass 3. Reported without that label they read as four failed reviews, which is exactly what provoked
> the complaint. Pass 3's critical, by contrast, was a genuine **MISS**, it had been true from the
> first minute, and Sweep 4 would have caught it.

## Step 7: Ask what to do with the findings

One `AskUserQuestion`:

1. **Apply all recommendations**, recommend this whenever there are CRITICALs
2. **Review one by one**
3. **Keep plan as-is**

**If a finding is a genuine product or design choice rather than a technical fix, ask about it as a
separate question in the same call.** The user decides scope; you decide correctness. Do not quietly
apply a scope decision, and do not sit on one either, an unasked question becomes the next pass's
NEW SCOPE critical.

## Step 8: Apply, targeted edits only

**Never regenerate the plan file.** An agent handed a whole document rewrites parts nobody asked about
and reconciles them wrongly, turning one round of fixes into the next round's defects.

1. Keep the plan's exact current content as `BEFORE`.
2. Group accepted findings by the **Section** each names. All findings on one heading are applied
   **together, in one pass**, that, not whole-file rewriting, is how overlapping fixes avoid clashing.
3. One `Edit` per section: `old_string` is that section's exact current text, `new_string` the
   replacement, keeping the section's existing voice, formatting and heading level. Distinct sections
   cannot collide.
4. `NEW (after: ...)` inserts immediately after the named heading, also as a single `Edit`.
5. **A Section heading not found verbatim: do not guess a location.** Leave it unapplied and say so
   plainly in the summary.
6. Re-read and confirm every difference from `BEFORE` falls inside a section you deliberately
   targeted. If anything else moved, say which section drifted and what it now says.

### If "Review one by one"

Walk the findings in severity order. For each, show severity, source, title, detail and proposed
change, then `AskUserQuestion`: **Yes, apply** / **Skip this one**. Afterwards report *"Applied N of M
(breakdown by severity). Skipped N."* and apply only the accepted ones by the procedure above.

### Always append to the plan

```markdown

---

## Review Notes (YYYY-MM-DD)

### Sweep Ledger, pass N
<the table from Step 5>

### Applied Changes, pass N
- <one line per applied recommendation>

### Acknowledged Risks
- <one line per skipped CRITICAL or WARNING, and per NEW SCOPE decision the user took>
```

**The ledger goes in the plan file, not only in chat.** A pass that cannot read what the last pass
checked cannot tell MISS from NEW SCOPE, and chat scrollback is not a record.

If "Keep plan as-is": confirm the plan is unchanged, but **still append the Sweep Ledger**, the
review was work, and the next pass needs it.

## Writing the output

The plan owner may not be a developer and reads these directly.

- **Lead with what it means for him:** what would have gone wrong, and what he has to decide.
- Plain English. Keep the precision, drop the vocabulary. Spell out any term the first time.
- **Plain is never vague.** If something is broken, unfinished or uncertain, say so in one plain
  sentence. Being brief is never a licence to soften a warning.
- Every finding names the file and line that proves it. He need not read them, but **an unprovable
  finding does not belong in the list.**
- **No invented severity.** One SUGGESTION labelled CRITICAL costs the whole review its credibility,
  and the credibility is the only thing that makes the next pass worth running.
