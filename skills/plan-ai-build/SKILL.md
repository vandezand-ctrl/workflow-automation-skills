---
name: plan-ai-build
description: Turn an automation specification into an implementation plan an AI coding tool can execute, and review that plan until it holds before any code is written. Use after design-automation, when the route is AI-built software or a scripted integration.
---

# Plan an AI build

AI coding tools write code fast. They also build the wrong thing fast. This skill writes the plan first and reviews it hard, so the build is boring.

## Inputs

`automation-spec.md` (from design-automation) and, for an existing system, access to its repository or documentation.

## Steps

1. **Write the plan** as `build-plan.md`:
   - Data model: tables or files, fields, who may read and write each.
   - Components and their order of build, smallest working slice first.
   - For each component: what it does, its inputs and outputs, and how it is tested.
   - Where AI is called: the prompt's job, the expected output format, the approval step and the fallback.
   - Secrets and configuration: where they live; never in the code.
   - What is out of scope.

2. **Review the plan** against six questions. Record each finding with the line it refers to:
   - Does every requirement in the specification map to a component?
   - Can each component be tested on its own, with the evaluation set where AI is involved?
   - Who can see or change which data, and is that enforced in the code, not just the screen?
   - What happens on failure: a tool is down, an input is malformed, the AI output is wrong?
   - Is anything built that the specification did not ask for?
   - Can the person who owns the result run and change it after go-live?

3. **Fix and repeat** until a review pass finds nothing new. Keep a short log of what changed per pass.

4. **Prototype before code where people will use a screen.** A clickable mock-up of the main screens, approved by the owner, before the build starts.

5. **Hand over** the approved plan to the coding tool in slices, with the tests for each slice.

## Output

`build-plan.md`, `plan-review-log.md`, and the approved prototype link or screenshots.

## Rules

- No code before the plan passes review.
- Every change after approval goes back through step 2 for the parts it touches.
