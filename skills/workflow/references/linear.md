# Optional Linear task tracking

Load for formal development or repair, including repository and skill maintenance, only when authorized Linear tools are exposed. Respect an explicit opt-out, read-only request, and host approval rules. Discussion, planning, investigation, PR introductions, and reviews do not start or mutate tracking unless the user asks to record them.

## Capability and task selection

1. Inspect the actual tool capabilities, not a fixed MCP server name. Without a Linear integration, skip these steps without a setup prompt, installation, authentication, or substitute tracker.
2. Confirm the target repository. Prefer an explicit Issue, then an existing repository/PR link, then a narrowly scoped search for the same problem. Confirm workspace and team from project context or the user; never copy another user's team, project, assignee, or workflow states. Ask when the destination or matching Issue is ambiguous. Do not enumerate unrelated workspaces or backlog history.
3. Reuse the matching Issue. Only create one after a successful search finds no corresponding task and the destination is clear. A formal implementation request permits this task-scoped tracking by default, unless the user or host restricts it; it does not permit creating teams/projects, reorganizing a backlog, or changing unrelated Issues.
4. Missing write capability, access errors, and failed searches are not evidence that an Issue is absent. Briefly report the limitation; do not create duplicates, claim a successful write, or silently treat a failed integration as unconfigured. Continue only independently authorized local work while a tracker decision is pending.
5. Before implementation, reread the current description, acceptance criteria, and relevant confirmed decisions. Use actual team statuses when a task-scoped transition is appropriate; do not post a separate comment just to announce that work started.

## Keep the Issue current

The description is the current task agreement, not an execution journal. Keep it focused on:

- the affected user or maintainer, triggering situation, observed problem, and consequence;
- the confirmed result, scope, and only the design decisions needed to understand it;
- observable acceptance criteria and the agreed delivery/completion condition.

Update the existing description when a confirmed decision changes that agreement. Preserve relevant user content and unresolved choices. Do not turn a hypothesis, proposed design, or planned verification into a confirmed fact. Use a small behavior-focused Mermaid diagram when it clarifies a lasting decision; follow [behavior-first explanation](explanation.md) then, not at tracker startup.

## Write back only material changes

- Comment for a consequential decision, a blocker needing attention, or a meaningful delivery/acceptance result. Skip routine progress, repeated checkpoints, command-by-command narration, and duplicate summaries.
- State the outcome, its effect on the task, remaining decision or limitation, and a useful PR/CI link. Report relevant failures and missing acceptance honestly, without repeating every prior caveat.
- Keep full command output, test counts, tool versions, commit reconciliation, environment detours, and cleanup receipts in CI or useful raw evidence. Include a narrow technical detail only when it changes a decision or is needed to reproduce the problem. Do not generate a separate prose report merely to have something to link.
- Read back a write before claiming it succeeded. Add only genuinely relevant task relationships; do not create dependencies or parent-child links for convenience.
- Reflect actual progress. Code written, tests passing, or a PR opened alone is not Done. Check the full agreed acceptance and delivery scope; when completion requires a merged PR, verify its integration into the target snapshot. Keep pending review, user acceptance, and unresolved failures visible.

When preparing or updating a PR for the task, load [Issue–PR relationship rules](linear-pr-links.md) then. Choose Resolves, Contributes, or Related from the actual delivery scope; do not preload the linking procedure at task startup.

Tracker access never grants commit, push, published review, merge, deployment, shared-instance changes, or resource cleanup authority.
