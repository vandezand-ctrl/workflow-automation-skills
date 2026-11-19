---
name: generate-backend
description: >-
  Act as the Handover Agent: read a frontend that's already been built with dummy/mock
  data (plus its PRD, if one exists), and produce exactly one deliverable, a
  Backend-dev-plan.md file that tells Claude Code, in dynamic sprints (S0 → Sn), how to
  build the real backend behind it. Trigger this whenever the user asks to generate the
  backend, create or write a backend dev plan / backend development plan, says "handover
  agent", "plan the backend", "spec out the API for this frontend", "what backend does
  this need", points at a generated frontend + PRD and asks for backend implementation
  guidance, or mentions /generate-backend. The plan always assumes FastAPI (Python 3.13,
  async) with MongoDB Atlas via Motor + Pydantic v2, no Docker, a single "main" git
  branch, and manual (not automated) testing after every task, flag this stack
  assumption to the user up front if their project clearly needs something else, since
  the skill will not silently substitute a different stack. This skill ONLY writes the
  plan document and then stops for the user's review, it never starts building,
  scaffolding, or coding the backend itself, even though an earlier version of this
  prompt did.
---

# generate-backend

## What this skill does
Acting as the "Handover Agent", a senior full-stack tech lead, this skill reads a
frontend that has already been built with dummy/placeholder data (plus its PRD, if one
exists) and writes exactly one file: `Backend-dev-plan.md`. That document is a
bullets-only, sprint-by-sprint (S0 → Sn) instruction set a later Claude Code session can
follow to build a real FastAPI + MongoDB Atlas backend behind the frontend. This skill's
job ends the moment that file is written and reported back, it does not scaffold, code,
or run anything itself.

## What this skill does NOT do
- Does not write or modify any backend code, `.gitignore`, config file, or any file
  other than `Backend-dev-plan.md`.
- Does not start building/executing the sprints after the plan is written. An earlier
  version of this prompt did that automatically, that step has been intentionally
  removed. The skill always stops and hands the plan to the user for review.
- Does not swap in a different tech stack quietly. The plan is always FastAPI /
  Python 3.13 / MongoDB Atlas / Motor / Pydantic v2 / no Docker, if the project
  obviously needs something else, say so and confirm before generating.
- Does not include backend features, endpoints, or data models that aren't visible in
  the frontend or required by the PRD.

## Workflow

### Step 1, Locate and read the frontend (and PRD, if any)
Ask the user for the frontend project path if it isn't already given. Read the actual
frontend code directly (pages/routes/components, not just file names), this is the
primary source of truth for every later section. Then look for a PRD (ask the user, or
check for common names like `PRD.md`, `requirements.md`, a project brief). If no PRD
exists, proceed frontend-only and say so in the plan's Executive Summary.

### Step 2, Load the plan template
Read `references/backend-plan-template.md` in this skill folder in full before drafting
anything. It holds the hard constraints, output rules, the 10-section document
structure, the S0 setup sprint, the S1 auth worked example, the S2→Sn pattern, and the
style/compliance checklist. Do not deviate from it or improvise a different document
shape.

### Step 3, Audit the frontend feature by feature
Build the Frontend Audit & Feature Map first (per screen/component: route, purpose,
data needed, required endpoint(s)/model(s), auth requirement). Every later section , 
API design, data model, sprints, must trace back to something in this audit. Omit
anything not actually present in the frontend or PRD.

### Step 4, Draft Backend-dev-plan.md
Follow `references/backend-plan-template.md` section by section: Executive Summary,
In-Scope & Success Criteria, API Design, Data Model, Frontend Audit & Feature Map,
Configuration & ENV Vars, Background Work (if needed), Integrations (if needed),
Testing Strategy, Dynamic Sprint Plan (S0→Sn). Bullets only, no tables or prose
paragraphs. Every task in every sprint needs both a Manual Test Step and a User Test
Prompt. Save the file as `Backend-dev-plan.md` in the frontend project's root (ask if
the location is unclear).

### Step 5, Report back and stop
Tell the user: the file path, a one-line count/summary of sprints and scope covered,
and explicitly that implementation has NOT started. Ask whether/when they want to move
to actually building it, that would be a separate, later step. Do not write any
backend code or begin Sprint S0 in this same turn.

## Strict rules
1. **One file only.** The only file this skill ever creates or edits is
   `Backend-dev-plan.md`. Never create a `.gitignore`, source code, or a second
   markdown file.
2. **Stop after the plan, always.** Never proceed to implement, scaffold, or execute
   any sprint automatically after writing the plan, this overrides any instinct to
   "keep going." Wait for the user's explicit go-ahead in a new request.
3. **Stack is fixed, flag, don't silently override.** FastAPI (Python 3.13, async),
   MongoDB Atlas via Motor + Pydantic v2, no Docker, no Celery/task queues
   (BackgroundTasks only if truly needed), single `main` git branch, `/api/v1/*` base
   path, manual testing after every task (not just sprints). If the frontend/PRD
   clearly implies a different stack, pause and confirm with the user before generating
   a plan built on the wrong assumptions.
4. **Bullets only** in the output document, no tables, no prose paragraphs.
5. **Only what's visible.** Never include a section, endpoint, model, or sprint for a
   feature that isn't actually present in the frontend or explicitly required by the
   PRD.
6. **Inline sensible defaults** for anything genuinely unspecified (naming, minor
   validation) rather than stalling the whole plan, but never use a "default" to
   quietly override one of the hard constraints in rule 3.

## Files in this skill
- `SKILL.md`, this file.
- `references/backend-plan-template.md`, the full `Backend-dev-plan.md` template:
  hard constraints, output rules, the 10-section document structure, the S0
  environment-setup sprint, the S1 auth worked example, the S2→Sn pattern, and the
  closing style/compliance checklist. Read in full at Step 2 before drafting.
