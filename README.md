# Workflow automation skills

Ten Claude skills for one job: finding where manual work slows a team down, automating it safely, and proving the result. They cover the whole cycle, from the first interview to the impact report, and two of them come with Python scripts.

## The skills

| Stage | Skill | What it does | Output |
|---|---|---|---|
| Discover | [`process-discovery-interview`](skills/process-discovery-interview/SKILL.md) | Prepares interviews with the people who do the work and turns answers into structured notes | Interview guide, notes, findings |
| Discover | [`map-workflow`](skills/map-workflow/SKILL.md) | Maps the process as people do it today, step by step | Step table, Mermaid flowchart by role, hands-on hours per month |
| Discover | [`analyse-process-log`](skills/analyse-process-log/SKILL.md) | Reads a system export and finds throughput times, waits, slow handoffs, rework and common paths. **Python script** | Process log analysis |
| Decide | [`find-automation-candidates`](skills/find-automation-candidates/SKILL.md) | Routes every step: remove, simplify, rule-based automation, AI with human approval, software, or keep manual | Ranked candidates with hours saved, risk, preconditions |
| Decide | [`automation-business-case`](skills/automation-business-case/SKILL.md) | One page with value, cost, payback, sensitivity, risks and the decision asked | Business case |
| Design and build | [`design-automation`](skills/design-automation/SKILL.md) | Specification with data, the AI's and the person's role, controls, test cases, measures and rollout | Automation specification |
| Design and build | [`plan-ai-build`](skills/plan-ai-build/SKILL.md) | Implementation plan for an AI coding tool, reviewed until it holds, prototype before code | Build plan and review log |
| Test | [`build-eval-set`](skills/build-eval-set/SKILL.md) | Real past cases with checked answers for every AI step, scored by script; blocks a change below the agreed pass rate. **Python script** | Evaluation set and report |
| Roll out | [`rollout-and-adoption`](skills/rollout-and-adoption/SKILL.md) | Pilot, training, owner after go-live, switch-off date for the old route, adoption tracking | Rollout plan |
| Measure | [`measure-automation-impact`](skills/measure-automation-impact/SKILL.md) | Before and after against the baseline, gaps explained, keep, improve or stop | Impact report |

## Principles

1. Map the process as people do it today, not as the policy describes it, and check it against the system's own data.
2. Get the process and the data right before automating; automation copies a broken process faster.
3. Use rules where rules are enough; use AI for unstructured inputs and drafts.
4. Put a named approver on every AI decision, with an audit log, a manual fallback and a scored evaluation set.
5. Switch the old route off on a fixed date, and measure the result against the baseline.

## Worked example

[`examples/supplier-invoices`](examples/supplier-invoices) runs a fictional 300-person distributor's invoice process through the skills: workflow map, process log analysis of 300 invoices, automation candidates, a business case with payback, and an evaluation report that shows the AI extraction is not yet ready for rollout. The company and all figures are invented.

## Scripts

Both scripts use the Python standard library only.

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

Then ask Claude, for example: "Prepare discovery interviews for our supplier invoice process", "Analyse this export from our ERP", or "Write the business case for the top three candidates".

## About

Made by [Jesse van de Zand](https://github.com/vandezand-ctrl). I redesign processes, automate them with AI and build the software a process needs. Case study: [hiring and onboarding tool for CarePal / Impact Guru](https://vandezand-ctrl.github.io/hiring-tool/).

MIT License.
