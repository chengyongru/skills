### Multi-phase or multi-PR plan

**Own the plan, not the code.** Deliver a checklist the user can inspect and an owner can execute. Do not implement it.

1. For an obvious small change, give a short plan and stop instead of manufacturing phases.
2. Ground the goal, current behavior, repository constraints, and dependencies. Settle empirical questions with an isolated [prototype](../code/prototype.md) only when experiments are authorized. Otherwise name the proposed probe and the unanswered question. Product and preference choices stay with the user.
3. Present the outcome, units in delivery order, and dependency graph. Distinguish independent units from stacked ones and give each an owner, allowed paths, prerequisites, one change, an observable result, and verification checkboxes. Use actual PR IDs only for existing PRs. Design larger or unmatched execution through [Figure it out](../../workflows/coordinate/playbook/workflow.md). Publication and landing need their own authorization.
4. Make each unit independently checkable. Name commands, scenarios, pass predicates, exact source snapshots, and evidence locations. A runtime claim needs a real supported interface, not just unit tests. Add performance checks when required or plausibly affected, with equivalent workloads, a baseline, noise controls, and a failure budget. Mark unrelated live/performance checks not applicable with a reason. Preserve user review gates and report unavailable required capabilities as blocked.
5. Check dependencies, paths, commands, ownership, and acceptance criteria, then hand back the plan and stop. Keep it in the conversation unless the user requests a file; use the selected path or an external run directory from the [workflow helper](../../scripts/workflow.py), never the installed plugin. Execution starts on the user's explicit go.

**Reply:** the plan, dependencies and review gates, what investigation established, and what remains unproven. Include a plan path only when a file was requested and written.
