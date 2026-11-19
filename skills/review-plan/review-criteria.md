# Review Criteria, routed

**Apply only the dimensions the plan's files actually reach.** Running all of them on every plan
produces boilerplate, and boilerplate is what a reader learns to skim. Say in one line which
dimensions you applied and why the others did not.

## Routing table

| What the plan touches | Dimensions to apply |
|---|---|
| Instruction / rules documents, `AGENT.md`, `CLAUDE.md`, `CONTRIBUTING.md`, operating constraints, skill files, prompt files | **0**, 5, 8 |
| Reference documents, architecture, API, data models, acceptance | **0** (lighter), 5, 8 |
| Task / process tooling, bead or ticket scripts, generators, doc validators | **0**, 3, 7, 8 |
| Application code | 1, 3, 5, 6, 8 |
| Database schema or migrations | 3, 4, 7, 8 |
| Auth, permissions, row-level security, secrets | **4 in full**, 3, 7 |
| Money or inventory ledgers, anything append-only | **3 in full**, 4, 7 |
| Network-facing endpoints or functions | 4, 2, 7 |
| Queries or lists over data that grows | 2, 3 |
| Build, CI, test tooling, git hooks | 7, 3, 5 |

**Dimension 8 (Scope discipline) applies to every plan.** It is cheap and it is the one the user cares
about most often.

Two or more rows can match. Take the union.

---

## 0. Instruction correctness

**Applies when:** the plan changes any document, rule, comment or prompt that tells a future person or
agent what to do.

**This dimension did not exist in the old criteria, and it is where the worked example's worst
findings lived.** A wrong sentence in a reference document misleads a reader; a wrong sentence in an
instruction document *changes what gets done*, silently, for as long as it stands.

### Check for
- **A claim about a tool that the tool does not honour.** Read the tool. The most dangerous version is
  a claim that is *nearly* true, a check that verifies half of what the sentence says it verifies.
- **What the tool cannot do, left unsaid.** A document that names a command as proof must say what
  that command does not see. Otherwise a reader stops checking at the point the document stopped
  describing.
- **The same rule stated in two places.** After this change, do they still agree? Two copies of one
  rule is not redundancy, it is a future contradiction with a delay fuse.
- **A measured figure written from memory.** Every number must be traceable to the thing that measures
  it, and the review should ask *"where was this read from?"*, not *"is this plausible?"*
- **A prohibition without its reason.** "Do not do X" decays into "X is fine really" within months.
  "Do not do X, because it discards Y even when Z" survives, because the reader can see the harm.
- **Softening instead of correcting.** If a document currently instructs a reader to do something
  harmful, *"be careful when doing X"* is not a fix. It has to stop saying it.
- **A rule with no evidence attached.** Rules that name the incident that produced them get followed;
  rules that assert get argued with.

### Anti-patterns
- **Faithful transcription**, the plan repeats its ticket's wording exactly, and the ticket was wrong.
  Fidelity to the task description is not correctness.
- **Two homes**, the corrected rule is written into both documents that carried the old one, which
  recreates the drift that made the fix necessary.
- **Documentation-only fix to a live instruction**, the document is corrected while the tool, script
  or template that emits the same instruction is left alone. The louder source wins.

### Severity guidance
- **CRITICAL:** the plan would leave two instruction documents in contradiction; the plan writes a
  claim about a tool that is false; the plan corrects the quieter of two sources and leaves the louder
  one giving harmful instructions.
- **WARNING:** a required convention of the target document is skipped (dated header, changelog line);
  a stated requirement is only half delivered; a figure is asserted before it is measured.
- **SUGGESTION:** wording that will read as ambiguous later; a missing cross-reference.

---

## 1. Architecture fit

**Applies when:** the plan adds or restructures application code.

### Check for
- New libraries or frameworks where the project already has an equivalent
- New patterns alongside established ones, a second state store, a second HTTP client, a second ORM
- Layer violations, business logic in route handlers, database queries in UI components
- Reinventing a utility that already exists in the project's shared modules, **grep before accepting
  the plan's claim that nothing exists**
- One concept implemented in two places where the project has a single home for it

### Severity guidance
- **CRITICAL:** an architecture that fundamentally contradicts established patterns, or bypasses a
  layer the project uses to enforce a rule
- **WARNING:** a minor new pattern where an existing one would have served
- **SUGGESTION:** naming or organisation could match conventions better

---

## 2. Scalability

**Applies when:** the plan adds queries, lists, or processing over data that grows. **Skip it
otherwise**, a fixed-size admin screen does not need a 10x analysis.

### Check for
- Queries inside loops (N+1)
- Fetching whole collections with no pagination or ceiling
- Missing indexes on columns used in `WHERE` / `ORDER BY`
- Worse-than-linear algorithms on data that grows
- Synchronous processing of work that should be queued
- **A volume assumption stated rather than computed.** Ask where the number came from; per-row
  multipliers compound in ways estimates miss.

### Severity guidance
- **CRITICAL:** queries in loops on growing tables, unbounded fetches, no pagination on a
  user-facing list
- **WARNING:** missing pagination on a currently-small internal list; a functional but suboptimal
  query
- **SUGGESTION:** optimisations that are not urgent

---

## 3. Bug surface area

**Applies when:** the plan changes behaviour. **In full** when it touches money, inventory, or any
append-only ledger.

### Check for
- Race conditions, concurrent modification with no locking or optimistic concurrency
- Missing error handling, what happens when the call fails, the row is absent, the write is rejected?
- Two sources of truth that can diverge
- Edge cases, empty input, maximum length, null, concurrent users, the degenerate maximum case
- Implicit ordering, "first A, then B" with nothing enforcing it
- Partial failure, step 3 fails after steps 1 and 2 committed
- **Content that will be destroyed by the mechanics of the change**, a replaced block containing
  live rules, a regenerated file containing hand-written text, a whole-file operation used where a
  section was meant

### Anti-patterns
- **Happy path only**, no failures, retries or degraded states described
- **Fire and forget**, async work with no error handling and no monitoring
- **Whole-file remedy for a partial problem**, the operation is wider than the defect and takes
  correct content with it

### Severity guidance
- **CRITICAL:** race conditions on writes, partial failure with no rollback, missing error handling on
  writes or deletes, a change that destroys content it was not meant to touch
- **WARNING:** edge cases affecting experience but not integrity
- **SUGGESTION:** defensive improvements

---

## 4. Security

**Applies when:** the plan touches auth, permissions, row-level security, secrets, uploads, or
anything reachable from a browser. **Skip it entirely otherwise and say so**, a security section on a
documentation plan is noise.

### Check for
- User input reaching SQL, shell, or HTML unescaped
- New endpoints or functions with no authentication check
- Authorization gaps, an authenticated user reaching another's data
- Secrets in source, in client-visible config, or in any variable inlined at build time
- Permissions granted more broadly than the feature needs
- **A definer-rights function or elevated-privilege path added without stating who may call it**

### Severity guidance
- **CRITICAL:** injection vectors, missing authentication on writes, secrets in source or client
  bundles, missing authorization checks
- **WARNING:** missing input validation, overly broad grants, no rate limiting
- **SUGGESTION:** defence in depth

---

## 5. Consistency

**Applies when:** the plan adds files or follows an existing pattern.

### Check for
- Naming and casing against siblings; file placement against project organisation
- Implementation symmetry, do similar features work the same way?
- Error handling style matching existing code
- **Conventions the target file keeps on itself**, a dated header stack, an ordering rule, a table
  marked "do not update"

### Severity guidance
- **CRITICAL:** rarely, only where inconsistency causes a runtime fault
- **WARNING:** inconsistency that will confuse the next reader or break a documented convention
- **SUGGESTION:** minor naming or organisation

---

## 6. Testing strategy

**Applies when:** the plan changes application code.

### Check for
- Are the critical paths identified for testing, and is the design testable?
- Are edge cases listed as scenarios rather than implied?
- Are failure paths tested, not only success?
- **What the tests cannot reach.** Layout at a given width, a database constraint, a policy refusal, a
  rendered string, many suites cannot see these, and a plan that treats a green run as full proof is
  wrong about its own evidence.
- **Guards that assert the shape of a file** rather than its behaviour, these go red on unrelated
  changes and are easy to miss when planning

### Anti-patterns
- **Test the mock**, never verifying the real integration
- **Coverage theater**, testing boilerplate instead of the logic that matters
- **No sad path**, every test expects success
- **Green means proved**, the plan claims the suite establishes something the suite structurally
  cannot see

### Severity guidance
- **CRITICAL:** no test strategy for a data-modifying feature, or a design with no seams for testing
- **WARNING:** missing edge cases, happy path only, a claim about what the tests prove that overstates
- **SUGGESTION:** organisation, additional assertions

---

## 7. Operational readiness

**Applies when:** the plan will be deployed, migrated, or run through a gate that can refuse it.

### Check for
- **Every gate that can refuse this work, and whether the plan satisfies it.** Sweep 2 gathers the
  evidence; this dimension judges it.
- Ordering constraints between steps, what breaks if they run in the wrong order?
- **State invalidated by an intervening action**, a token, snapshot, checkpoint or lock that a later
  step silently voids
- Reversibility: is the migration reversible, is there a rollback point?
- Are errors logged with enough context to diagnose?
- Manual steps: are they in the right hands, and are they at the top of the handover?
- Realistic timing, a plan that promises a duration it cannot meet produces a false alarm mid-build

### Anti-patterns
- **Big bang**, everything at once, no rollback
- **Silent failure**, errors swallowed with no logging or surfacing
- **Irreversible migration**, schema changes that cannot be undone
- **Documented mechanism, undocumented gate**, the plan follows the documented procedure, but the
  code enforces a different condition, so the documented step passes and the commit is still refused

### Severity guidance
- **CRITICAL:** irreversible migration with no rollback; a step order that voids a required
  precondition; a plan that a gate will refuse as written
- **WARNING:** missing structured logging, no monitoring, manual steps buried at the bottom
- **SUGGESTION:** flags, log context, dashboards

---

## 8. Scope discipline

**Applies to every plan.**

### Check for
- Does every change trace to a stated requirement?
- Premature abstraction, extension points for needs that do not exist
- "While we're at it" additions
- **The opposite failure, which the user cares about more:** does the plan wrap a small change in
  ceremony it does not need? A six-number documentation edit does not need a spec, a branch and a
  review cycle.
- **A stated requirement quietly dropped** to make the work smaller, scaling down is the user's
  decision, not the plan's

### Anti-patterns
- **Future-proofing**, building for hypothetical requirements
- **Kitchen sink**, unrelated improvements bundled in
- **Ceremony inflation**, process weight out of proportion to risk
- **Silent narrowing**, the plan drops part of the ask without saying so

### Severity guidance
- **CRITICAL:** rarely, only where scope expansion introduces real risk, or where a requirement was
  dropped without telling the user
- **WARNING:** additions that add complexity without justification; ceremony out of proportion
- **SUGGESTION:** simplification, removing unnecessary abstraction
