# Workflow automation skills

Seventeen Claude skills for one job: finding where manual work slows a team down, automating it safely, and proving the result. They cover the whole cycle, from the first interview to the impact report, including how AI-built software gets planned, reviewed and signed off. Two come with Python scripts.

## The skills

| Stage | Skill | What it does |
|---|---|---|
| Discover | [`process-discovery-interview`](skills/process-discovery-interview/SKILL.md) | Prepares interviews with the people who do the work and turns answers into structured notes |
| Discover | [`thematic-analysis`](skills/thematic-analysis/SKILL.md) | Six-phase qualitative analysis of interview notes and transcripts (Braun and Clarke), written up with a thematic map |
| Discover | [`map-workflow`](skills/map-workflow/SKILL.md) | Maps the process as people do it today: step table, flowchart by role, hands-on hours per month |
| Discover | [`analyse-process-log`](skills/analyse-process-log/SKILL.md) | Reads a system export and finds throughput times, waits, slow handoffs, rework and common paths. **Python script** |
| Decide | [`find-automation-candidates`](skills/find-automation-candidates/SKILL.md) | Routes every step: remove, simplify, rule-based automation, AI with human approval, software, or keep manual |
| Decide | [`automation-business-case`](skills/automation-business-case/SKILL.md) | One page with value, cost, payback, sensitivity, risks and the decision asked |
| Design | [`design-automation`](skills/design-automation/SKILL.md) | Specification with data, the AI's and the person's role, controls, test cases, measures and rollout |
| Design | [`flowy`](skills/flowy/SKILL.md) | Flowcharts, system diagrams and UI wireframes as editable HTML files |
| Build with AI | [`generate-backend`](skills/generate-backend/SKILL.md) | Writes the backend development plan behind a frontend that already exists |
| Build with AI | [`review-plan`](skills/review-plan/SKILL.md) | CTO-level review of an implementation plan with evidence sweeps and a ledger, so repeat passes converge |
| Build with AI | [`refine-plan`](skills/refine-plan/SKILL.md) | Loops that review and fixes the plan until it passes, then starts the work |
| Build with AI | [`CTOcheck`](skills/CTOcheck/SKILL.md) | One-off review of a plan, diff or branch with a ship, patch or rethink verdict |
| Build with AI | [`mockup-prebuild`](skills/mockup-prebuild/SKILL.md) | Publishes a clickable before-and-after prototype for approval before any code is written |
| Build with AI | [`mockup-signoff`](skills/mockup-signoff/SKILL.md) | Publishes screenshots of what a finished branch changed, for sign-off before merge |
| Test | [`build-eval-set`](skills/build-eval-set/SKILL.md) | Real past cases with checked answers for every AI step, scored by script; blocks a change below the agreed pass rate. **Python script** |
| Roll out | [`rollout-and-adoption`](skills/rollout-and-adoption/SKILL.md) | Pilot, training, owner after go-live, switch-off date for the old route, adoption tracking |
| Measure | [`measure-automation-impact`](skills/measure-automation-impact/SKILL.md) | Before and after against the baseline, gaps explained: keep, improve or stop |

The build stage (generate-backend, review-plan, refine-plan, CTOcheck, the two mockup skills and flowy) is the review loop I use for the software I build with AI. `thematic-analysis` builds on the MIT-licensed thematic analysis skill by Chuah Kee Man; its licence is in the skill folder.

## Principles

1. Map the process as people do it today, not as the policy describes it, and check it against the system's own data.
2. Get the process and the data right before automating; automation copies a broken process faster.
3. Use rules where rules are enough; use AI for unstructured inputs and drafts.
4. Put a named approver on every AI decision, with an audit log, a manual fallback and a scored evaluation set.
5. No code before the plan passes review, and no merge before the people who use it have seen the screens.
6. Switch the old route off on a fixed date, and measure the result against the baseline.

## Worked example

[`examples/supplier-invoices`](examples/supplier-invoices) runs a fictional 300-person distributor's invoice process through the skills: workflow map, process log analysis of 300 invoices, automation candidates, a business case with payback, and an evaluation report that shows the AI extraction is not yet ready for rollout. The company and all figures are invented.

## Scripts

The process log and evaluation scripts use the Python standard library only.

```
python skills/analyse-process-log/scripts/analyse_process_log.py process-log.csv --out process-log-analysis.md
python skills/build-eval-set/scripts/run_evals.py expected.csv actual.csv --numeric total_amount --min-pass 0.9 --out eval-report.md
```

## Install

In Claude Code:

```
/plugin marketplace add vandezand-ctrl/workflow-automation-skills
/plugin install workflow-automation@vandezand-ctrl
```

Or copy a skill folder from `skills/` into your project's `.claude/skills/` folder.

## About

Made by [Jesse van de Zand](https://github.com/vandezand-ctrl). I redesign processes, automate them with AI and build the software a process needs. Case study: [hiring and onboarding tool for CarePal / Impact Guru](https://vandezand-ctrl.github.io/hiring-tool/).

These skills come from the library of 40+ skills I keep for my work. The rest of that library stays private: some skills are written for one organisation or client, and others come from Reforge courses whose licence does not allow sharing them.

MIT License, except where a skill folder carries its own licence.
