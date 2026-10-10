---
name: herdr-worktree-right
description: Open the active Git worktree in the pane immediately to the right of the calling Herdr pane, reusing that pane when it exists. Use when the user asks to open the current worktree in a right-hand Herdr pane on Linux or Windows. Requires HERDR_ENV=1.
---

# Herdr Worktree Right

Pass the task's active worktree directory explicitly, rather than the skill directory or an unrelated checkout. Require `HERDR_ENV=1` and resolve the caller through inherited `HERDR_PANE_ID` or an explicitly verified pane ID.

On Linux, run [scripts/open-worktree-right.py](scripts/open-worktree-right.py) with Python 3 (standard library only; no PowerShell dependency):

```bash
python3 <skill-directory>/scripts/open-worktree-right.py --cwd <active-worktree-path>
```

On Windows, run [scripts/open-worktree-right.ps1](scripts/open-worktree-right.ps1) with PowerShell 7:

```powershell
& <skill-directory>/scripts/open-worktree-right.ps1 -Cwd $PWD.Path
```

The helper resolves the Git worktree and calling pane, reuses the right-hand pane or creates it, and verifies its directory while preserving focus. It leaves an existing pane untouched when changing directories would interrupt a process or the shell prompt cannot be recognized. It creates no worktrees and starts no agents.

Use `--dry-run` on Linux or `-DryRun` on Windows for read-only inspection. Report `status`, `pane_id`, and `worktree` from the returned JSON.

## Recover stale caller context

A shared agent daemon can retain `HERDR_PANE_ID` from an earlier pane. `pane_not_found` from `pane current --current` means caller resolution failed before looking for a right-hand neighbor. Once the caller is resolved, the helper creates a missing neighbor normally.

When inherited context is missing, stale, or belongs to another conversation:

1. Run `herdr pane list` and read candidate panes with `herdr pane read <id> --source recent-unwrapped --lines 80`. Match the current conversation; use process information as supporting evidence when available. UI focus and a shared repository directory alone do not establish caller identity.
2. Retry the helper with `--caller-pane-id <verified-id>` on Linux or `-CallerPaneId <verified-id>` on Windows. Pass the verified ID explicitly while preserving the inherited environment.
3. If evidence cannot identify the caller uniquely, explain the ambiguity and request the caller pane ID. Stop further mutations on other helper failures and keep any pane already created available for inspection.
