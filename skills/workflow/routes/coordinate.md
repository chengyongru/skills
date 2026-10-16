# Coordinate bounded work

Use direct execution for small tasks. Choose orchestration only when the requested scope benefits from it; a no-subagent instruction applies to every route.

| Need | Workflow or playbook |
|---|---|
| Design an evidence-based workflow where no narrower route fits | [Figure it out](../workflows/coordinate/playbook/workflow.md) |
| Partition coverage or run an explicitly bounded race | [Swarm](../workflows/coordinate/swarm/workflow.md) |
| Compare candidate artifacts and combine the best parts | [Arena](../workflows/coordinate/arena/workflow.md) |
| Keep or audit a decision trail (`show-me-your-work`) | [Decision log](../workflows/coordinate/decision-log/workflow.md) |
| Write a multi-phase plan without implementing | [Multi-phase plan](../playbooks/coordinate/multi-phase-plan.md) |
| Resume prior work after reconciling actual state | [Session pickup](../playbooks/coordinate/session-pickup.md) |
| Pause safely and leave a handoff | [Pause safely](../playbooks/coordinate/pause-safely.md) |
| Drive one longer authorized task to a finite predicate | [Bounded run](../playbooks/coordinate/autonomous-run.md) |
| Coordinate multiple authorized tracks | [Orchestrate](../playbooks/coordinate/orchestrate.md) |
| Coordinate independent PR lifecycles | [Multiple PRs](../playbooks/coordinate/autopilot-full.md) |
| Prepare a dependency stack for operator review | [PR stack](../playbooks/coordinate/autopilot-stack.md) |

Give each child only its bounded task, the [worker contract](../references/worker.md), and selected workflow/reference paths. Do not send the whole catalog. Keep one writer per branch or artifact, inspect reports, and retain ownership of integration and final proof. Private task IDs are not durable sessions. Checkpoints do not keep execution alive after runtime limits or restart, and a playbook never grants external-action permission.
