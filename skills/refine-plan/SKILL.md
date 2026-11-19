---
name: refine-plan
description: Iteratively reviews and auto-refines the active plan-mode plan until it passes CTO review (0 CRITICAL, ≤1 WARNING) or hits the 5-iteration cap, then calls ExitPlanMode to execute. Plan-mode-only, must be invoked from within plan mode after the initial plan is written. Pauses to ask the user only when a recommendation is a real design/feature choice (not a technical fix). Use when the user invokes /refine-plan or asks to "harden", "auto-refine", or "loop-review" the active plan.
argument-hint: (none, operates on the plan-mode-designated plan file)
allowed-tools: Read, Glob, Grep, Bash, AskUserQuestion, Edit, Write, Agent, ExitPlanMode
user-invocable: true
---

Loop `/review-plan`'s review logic against the active plan until it's clean, auto-applying technical fixes and pausing only for design-level choices. On convergence, call `ExitPlanMode` to hand the cleaned plan back for execution.

This skill **inlines** `/review-plan`'s review steps (does not call `/review-plan` via the Skill tool, that would prompt the user every iteration). It reuses `${CLAUDE_PLUGIN_ROOT}/skills/review-plan/review-criteria.md` (the `review-plan` skill in this same plugin) as the single source of truth for review criteria.

## Step 0: Preconditions (run before anything else)

1. **Confirm plan mode is active.** If not, stop immediately with this message and make no edits:
   > `/refine-plan` must be invoked from within plan mode. Enter plan mode first (Shift+Tab → Plan Mode), write your initial plan, then invoke this skill.

2. **Identify the plan-mode-designated plan file.** This is the path the harness wrote into the plan-mode system message, the same file `ExitPlanMode` will read from. Save as `PLAN_PATH`.

3. **Ignore `$ARGUMENTS`.** If the user passed a path, warn them once that the argument is unused because `refine-plan` always operates on the active plan-mode file (the only file `ExitPlanMode` will reflect).

4. **Verify the file exists and is non-empty.** If not, stop with a helpful message, no edits.

## Step 1: Read the plan

Read `PLAN_PATH` in full.

## Step 2: Gather project context (once)

Gather enough context to ground every iteration's review. Do this ONCE, not per iteration.

1. Read `CLAUDE.md` if it exists in the project root
2. Glob the project root for package manifests (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Gemfile`, `pom.xml`, `composer.json`) and read any found
3. Read config files if present: `tsconfig.json`, `.eslintrc.*`, `biome.json`, `prettier.config.*`
4. Run `git log --oneline -10 2>/dev/null` (use the Bash tool, Git Bash, not PowerShell)
5. If the plan references specific existing files, read those files

Capture the gathered material as `PROJECT_CONTEXT` (a concise summary you can paste into every iteration's subagent prompt).

## Step 3: Initialize loop state

- `iteration = 0`
- `MAX_ITERATIONS = 5`
- `history = []`, list of `{iteration, critical, warning, finding_titles_set}` for content-aware oscillation detection
- `acknowledged_risks = []`, list of `{title, severity, dimension, recommendation}` the user has explicitly skipped; passed into every subsequent review subagent so they aren't re-flagged
- `applied_log = []`, list of `{iteration, applied: [titles], unapplied: [titles], acknowledged: [titles]}` for the audit trail written to the plan
- `sections_changed_last_round = []`, the exact plan headings edited by the previous iteration's apply step. Empty on the first pass. This is what scopes each later review (4a-i), so it must be recorded accurately in 4h.

## Step 4: The refinement loop

Repeat until a break condition fires:

### 4a. Spawn a fresh review subagent

Use the `Agent` tool with `subagent_type: general-purpose`. The prompt must contain:

- The instruction to load `${CLAUDE_PLUGIN_ROOT}/skills/review-plan/review-criteria.md` and read the plan at `PLAN_PATH`
- The inlined `PROJECT_CONTEXT` (don't ask the agent to re-gather)
- The inlined `acknowledged_risks` list as JSON, with this instruction:
  > The user has explicitly considered and accepted these risks. Do NOT re-flag them. You may flag genuinely new findings that happen to touch the same dimension.
- The instruction to evaluate against all 8 dimensions (Architecture fit, Scalability risks, Bug surface area, Security, Consistency, Testing strategy, Operational readiness, Scope discipline)
- **The review scope for this iteration**, see 4a-i. This differs between the first pass and every later one, and getting it right is what keeps the loop from re-auditing prose nobody touched.
- A request for this exact tail format at the end of the reply:

```
---
MACHINE_SUMMARY: critical=N warning=N suggestion=N
FINDINGS_JSON:
[
  {"severity": "CRITICAL", "dimension": "...", "title": "...", "detail": "...", "recommendation": "...", "section": "### Exact Heading Text", "after_section": null, "choice_importance": 0-10}
]
```

- An explanation of `section` and `after_section`, which are what make targeted application possible. Include this verbatim:
  > `section` is the EXACT heading line of the plan section your fix belongs in, copied character-for-character out of the plan including its `#` markers, for example `### 4. Fail loudly`. Your fix will be applied to that section and nothing else, so name the one place the change belongs. If a fix genuinely requires changes in two different sections, emit two findings, one per section. If it needs a brand-new section, set `section` to `"NEW"` and set `after_section` to the exact heading it should be inserted after. Otherwise leave `after_section` as null. A finding whose `section` cannot be found verbatim in the plan cannot be applied, so copy it, don't paraphrase it.

- An explanation of `choice_importance` with concrete examples:
  - **Score 1-3** (technical, auto-apply): add input validation, fix N+1 query, add error handling, add an index, refactor for testability, add logging
  - **Score 7-10** (design choice, ask user): pick library X vs Y, change UX flow, drop/add a feature, change data-model semantics, cut scope, change auth model

#### 4a-i. Review scope, full on the first pass, targeted afterwards

**First pass (`iteration == 0`): full review.** Review the entire plan, exactly as this skill has always done. Include no scope restriction in the prompt.

**Every later pass (`iteration >= 1`): scoped review.** Include `sections_changed_last_round` in the prompt along with this instruction, verbatim:

> The previous round edited exactly these sections, and nothing else: [list]. Your review has two jobs, and only two:
>
> 1. **Review those sections.** Are the applied fixes correct, complete, and free of new defects?
> 2. **Check whether those edits contradict, duplicate, or invalidate anything ELSEWHERE in the plan.** Read the whole plan to do this. A change in one place quietly breaking a claim in another is the most common failure in this loop, and this check is the only thing that catches it.
>
> What you must NOT do: hunt for new issues in sections nobody touched. Those were reviewed in full on the first pass and have not changed since. Re-auditing them produces findings that sound real but were already considered and accepted, and that is precisely why this loop used to run all the way to its cap.
>
> If the applied fixes hold and contradict nothing elsewhere, **report zero findings.** At this stage zero is the expected outcome, not a failure to be thorough.

If `sections_changed_last_round` is empty when it shouldn't be, fall back to a full review and say so in the summary rather than reviewing nothing.

### 4b. Parse the subagent's reply

Locate `MACHINE_SUMMARY:` and `FINDINGS_JSON:` and extract counts + findings array.

- **On parse failure (first time):** retry once with a follow-up subagent prompt:
  > Your previous response missed the `MACHINE_SUMMARY:` / `FINDINGS_JSON:` tail. Re-emit your findings using exactly this format: [paste format].
- **On parse failure (second time):** abort with status `PARSE_FAILED`. Surface the raw subagent output to the user. **Do NOT call `ExitPlanMode`.**

### 4c. Record history

Append `{iteration, critical, warning, finding_titles_set}` to `history` (titles set = set of finding titles this round, used by 4e).

### 4d. Check convergence, BEFORE the apply step

If `critical == 0 AND warning ≤ 1`: break with status `CONVERGED`.

This means a clean first iteration exits immediately without writing any audit-log noise to the plan.

### 4e. Check oscillation, content-aware

If `iteration ≥ 2` AND `history[iteration].finding_titles_set == history[iteration - 2].finding_titles_set` (exact set equality on titles): break with status `OSCILLATING`.

Pure count equality is not enough, different findings can share counts.

### 4f. Partition findings by `choice_importance`

- `auto_apply` = findings where `choice_importance < 7`
- `ask_user`  = findings where `choice_importance ≥ 7`

### 4g. If `ask_user` is non-empty, pause for the user

For each item in `ask_user`, present via `AskUserQuestion`:

- **Question:** title + detail + recommendation, framed as "This is a design choice, apply?"
- **Two options only:**
  - **Yes, apply**, add to `auto_apply`
  - **Skip, acknowledge risk**, append `{title, severity, dimension, recommendation}` to `acknowledged_risks` (consumed by future iterations per 4a)

### 4h. Apply as targeted edits to the sections the findings name

**Never regenerate the whole plan.** Every finding names the section it belongs in (`section`, from 4a), and its fix may touch that section and nothing else.

This is the most important rule in this skill. Whole-file regeneration is how a refinement loop starts finding bugs in its own previous edits: an agent handed the entire document rewrites paragraphs it was never asked about and has not reasoned about, and reconciles them wrongly. Two of the worst findings in the run that prompted this rule, a file described as both edited and untouched, and a safety check that cancelled the fix sitting beside it, were created that way and did not exist before the rewrite.

1. **Snapshot.** Read `PLAN_PATH` and keep its exact current content as `BEFORE`.

2. **Resolve every `section` anchor** against `BEFORE`. If a heading cannot be found verbatim (a previous round renamed it, or the reviewer paraphrased), send ONE follow-up to the review subagent asking it to re-state the anchor using a heading that appears verbatim in the plan. If it still cannot be resolved, leave that finding **unapplied**, record it in the audit entry and say so in the final summary. **Never guess a location.**

3. **Group findings by section.** All findings targeting the same heading are applied **together, in one pass, by one agent.** This, not whole-file rewriting, is how overlapping fixes are kept from clashing. The original reason for regenerating the file is fully addressed by this grouping.

4. **For each group, spawn a fresh `Agent` (`general-purpose`) given ONLY:**
   - the current text of that one section (its heading line through to the next heading of the same or higher level, exclusive)
   - that section's findings as JSON
   - this instruction:
     > Rewrite this ONE section to incorporate every finding's recommendation. Return only the replacement text for this section, starting with its heading line, no preamble, no fences, no commentary. Keep the section's existing voice, formatting and heading level. Do not invent changes beyond what the findings ask for. You have deliberately not been shown the rest of the plan; do not attempt to change anything outside this section, and do not add cross-references to sections you cannot see.

5. **Write each section back with a single `Edit`**, `old_string` is that section's exact current text, `new_string` is the returned replacement. One edit per section, and because each targets a distinct section they cannot collide.

6. **For `section: "NEW"` findings**, insert the new section immediately after the heading named in `after_section`, again with a single `Edit`.

7. **Verify nothing else moved.** Re-read `PLAN_PATH` as `AFTER`, and confirm every difference between `BEFORE` and `AFTER` falls inside a section that was deliberately targeted. The cheap check: for each untargeted section, assert its text is byte-identical in `BEFORE` and `AFTER`.
   **If anything outside the targeted sections changed, stop the loop immediately** with status `SCOPE_VIOLATION`, tell the user exactly which section drifted and what it now says, and do **NOT** call `ExitPlanMode`. This check is the guard that catches an apply agent reaching further than it was told to.

8. **Record `sections_changed_last_round`** = the exact list of headings actually edited (including any newly inserted ones). The next iteration reads this to scope its review (4a-i), so an inaccurate list silently breaks scoping.

### 4i. Record this iteration's audit entry

Append to `applied_log`:
```
{
  iteration: N,
  applied: [list of applied finding titles],
  unapplied: [titles whose section anchor could not be resolved],
  acknowledged: [list of titles the user skipped this iteration],
  sections_edited: [exact headings edited this iteration]
}
```

### 4j. Increment and check the cap

`iteration += 1`. If `iteration ≥ MAX_ITERATIONS`: **do one final review pass** (re-run steps 4a-4c only, no further apply) to measure the post-apply state. Then:
- If the post-final-apply review meets the convergence threshold: break with `CONVERGED`
- Else: break with `CAPPED` using the post-apply counts

### 4k. Loop

Otherwise return to 4a.

## Step 5: Write the audit section to the plan

After the loop ends (any exit status **except** `PARSE_FAILED`), append a single consolidated section to `PLAN_PATH`, named to match `/review-plan`'s convention:

```markdown

---

## Review Notes (refinement run, YYYY-MM-DD)

### Iteration 1
- Applied: [title]; [title]
- Acknowledged risks: [title]; [title]

### Iteration 2
- Applied: [title]; [title]
- Sections edited: [heading]; [heading]
- Acknowledged risks: (none)

### Status: CONVERGED | OSCILLATING | CAPPED | SCOPE_VIOLATION
- Final: N critical, M warning, K suggestion
- Iterations: N of 5
- Unapplied (anchor unresolved): [title], or (none)
```

If the loop converged on iteration 1 with zero findings to apply, you may skip this section entirely, the plan was clean as written.

## Step 6: Handle exit status

- **`CONVERGED`**, print a 1-2 line summary ("Plan refined in N iterations. Final: 0 critical, K warning."), then call `ExitPlanMode`.
- **`OSCILLATING`**, print a summary explaining the same finding titles surfaced twice 2 iterations apart, show the last verdict's findings, and **stop without calling `ExitPlanMode`**.
- **`CAPPED`**, print a summary ("Hit 5-iteration cap with N critical, M warning remaining"), show last findings, and **stop without calling `ExitPlanMode`**.
- **`SCOPE_VIOLATION`**, an apply agent changed text outside the sections it was given (caught by 4h step 7). Name the section that drifted, show what it now says versus what it said before, and **stop without calling `ExitPlanMode`**. Treat this as a defect in the loop, not in the plan: the user should be told the plan may now contain an edit nobody asked for.
- **`PARSE_FAILED`**, print the raw subagent output that wouldn't parse and the iteration it failed on, and **stop without calling `ExitPlanMode`**. No Review Notes section is written.

## Critical notes

1. **Plan-mode-only, enforced in Step 0.** `ExitPlanMode` requires plan mode active and acts on the harness-designated plan file. Any other path won't be reflected. Step 0 fails fast before any edits if plan mode is not active.

2. **Spawn a fresh `Agent` every iteration**, for the review (4a) and for each section's apply (4h). A fresh agent isn't biased by previous rounds. Note the deliberate asymmetry: the reviewer reads the whole plan, an apply agent sees only its one section.

3. **Single source of truth for criteria.** The review subagent loads `review-criteria.md` from `/review-plan`'s directory. If criteria are later edited, both skills stay in sync.

4. **The `choice_importance` bar.** Include the concrete examples (Step 4a) verbatim in the subagent prompt. Without examples the subagent will either over-pause (annoying) or never pause (defeats the carve-out).

5. **Acknowledged risks really are passed in.** Step 4a's prompt MUST include the `acknowledged_risks` list. This is what prevents the loop from re-flagging items the user has consciously waved through.

6. **Counts come from the parseable tail, not prose.** The wrapper parses `MACHINE_SUMMARY:`, the human-readable summary is for the user. They must agree, but the machine line is the contract.

7. **Apply is targeted `Edit`s, never a whole-file `Write`.** This reverses an earlier version of this skill, and the reversal is the point. That version regenerated the entire plan each round to avoid overlapping edits, and in doing so became the loop's main source of new defects, because an agent handed the whole document rewrites parts it was never asked about. Overlapping fixes are now handled by **grouping all findings for a section and applying them in one pass** (4h step 3), which solves the original problem without touching anything else. Step 4h step 7 then proves nothing else moved. If you are tempted to "just regenerate it, it's cleaner", that is the exact instinct that caused an eight-round run to finish with findings still open.

8. **Scoped review is not a shortcut, and it is not blind.** From the second pass onward the reviewer still reads the entire plan; what changes is its mandate, review what moved, and check whether what moved broke anything elsewhere. It is explicitly told not to hunt for fresh issues in untouched prose, because that prose was fully reviewed on the first pass. Do not "improve" this by restoring a full re-audit every round; that is what the change was made to stop.

9. **Don't call `/review-plan` via the `Skill` tool.** It ends with an interactive `AskUserQuestion` the wrapper can't auto-answer. Criteria are reused via the file reference, not the skill invocation.
