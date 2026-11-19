# Workflow automation skills

Three Claude skills for one job: finding where manual work slows a team down, and automating it safely.

| Skill | What it does | Output |
|---|---|---|
| `map-workflow` | Maps a workflow as people do it today, step by step, from interviews, notes, SOPs or screenshots | `workflow-map.md` with a step table, a Mermaid flowchart by role and hands-on hours per month |
| `find-automation-candidates` | Scores every step and routes it: remove, simplify, rule-based automation, AI with human approval, software, or keep manual | `automation-candidates.md` with hours saved, risk, effort and preconditions per step |
| `design-automation` | Turns one candidate into a buildable specification | `automation-spec.md` with data, the AI's and the person's role, controls, test cases, success measures and rollout |

The skills follow five principles:

1. Map the process as people do it today, not as the policy describes it.
2. Get the process and the data right before automating; automation copies a broken process faster.
3. Use rules where rules are enough; use AI for unstructured inputs and drafts.
4. Put a named approver on every AI decision, with an audit log and a manual fallback.
5. Measure the result against the baseline from the map.

## Example

[`examples/supplier-invoices`](examples/supplier-invoices) shows the output of the first two skills for a fictional 300-person distributor. The company and all figures are invented for illustration.

## Install

In Claude Code:

```
/plugin marketplace add vandezand-ctrl/workflow-automation-skills
/plugin install workflow-automation@vandezand-ctrl
```

Or copy a skill folder from `skills/` into your project's `.claude/skills/` folder.

Then ask Claude, for example: "Map our supplier invoice process from these interview notes", followed by "Find the automation candidates" and "Design the automation for step 3".

## About

Made by [Jesse van de Zand](https://github.com/vandezand-ctrl). I redesign processes, automate them with AI and build the software a process needs.

MIT License.
