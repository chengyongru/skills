---
name: herdr-scode-delegate
description: Delegate a bounded background task from the current scode/Codex session to another scode session in a Herdr tab or pane. Use when the user asks to open another pane or tab, spawn another scode, or assign work without supervising it. Requires a Herdr-managed pane and the local PowerShell scode launcher.
---

# Herdr scode Delegate

Launch the user's `scode` PowerShell function as the canonical Codex entrypoint, submit one task, and return control to the current session without waiting for completion.

## Choose the target

- Honor an explicit `pane` or `tab` request.
- Default to a background tab for independent asynchronous work; it preserves the current layout.
- Use a sibling pane for short, closely related work that benefits from side-by-side visibility. Let the helper choose `right` or `down` unless the user specifies it.
- Keep the current workspace and cwd unless the user requests another location.
- Remember that tabs and panes share the same filesystem. Delegate concurrent writes only when file ownership is clearly disjoint. For overlapping or uncertain writes, keep the work local or ask whether to create an isolated worktree.

## Delegate

1. Confirm `HERDR_ENV=1` and select a short semantic name such as `review-api`.
2. Turn the request into a self-contained prompt containing the exact outcome, relevant paths and constraints, required verification, and this contract: preserve existing changes, stay within scope, work autonomously, and leave a concise result in the worker session. Tell it to ask one concise question only if genuinely blocked.
3. Resolve `scripts/delegate-scode.ps1` relative to this skill and run:

```powershell
$result = & <helper> -Name "review-api" -Task $task -Placement tab -Cwd $PWD.Path |
    ConvertFrom-Json
```

Use `-Placement pane` and optionally `-Direction right|down` when appropriate. The helper creates the target without focusing it, runs `scode`, waits only for Herdr startup detection, assigns a unique agent name, and submits the prompt without `--wait`.

4. Report `agent_name`, `tab_id`, `pane_id`, and cwd from `$result`, then stop supervising. Do not poll, wait for completion, or read the worker unless the user asks for status or the worker becomes blocked.

## Revisit delegated work

Herdr marks unseen completed work as `done` and questions as `blocked`. On an explicit status request, use `herdr agent get <agent_name>` and read recent unwrapped output only when useful. Focus the worker only when requested. Never close a worker target you did not create or the user did not ask to close.
