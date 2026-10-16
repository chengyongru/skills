# Environment operations

These workflows require their actual local tools and environment. Check those prerequisites before changing panes or launching an external agent.

| Explicit request | Workflow |
|---|---|
| Open or reuse the right-hand Herdr pane for the current worktree | [Worktree on the right](../workflows/environment/worktree-right/workflow.md) |
| Delegate a bounded background task to another scode session in Herdr | [Herdr scode delegation](../workflows/environment/delegate/workflow.md) |

Herdr scode delegation is not native nanobot subagent execution and does not acquire native task IDs or model controls. Use it only when the user requests that external scode/Herdr operation. For ordinary private parallel work use the [coordinate route](coordinate.md); never silently substitute one mechanism for the other or stop an existing user pane to make room.
