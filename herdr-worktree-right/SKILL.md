---
name: herdr-worktree-right
description: Open the active Git worktree in the pane immediately to the right of the calling Herdr pane, reusing that pane when it exists. Use when the user asks to open the current worktree in a right-hand Herdr pane. Requires HERDR_ENV=1 and PowerShell 7.
---

# Herdr Worktree Right

Run [scripts/open-worktree-right.ps1](scripts/open-worktree-right.ps1) with the agent's active working directory, before changing directories for tools or skill resources:

```powershell
& <skill-directory>/scripts/open-worktree-right.ps1 -Cwd $PWD.Path
```

The helper resolves the Git worktree and calling pane, reuses the right-hand pane or creates it, and verifies its directory while preserving focus. It leaves an existing pane untouched when changing directories would interrupt a process or the shell prompt cannot be recognized. It creates no worktrees and starts no agents.

Use `-DryRun` for read-only inspection. Report `status`, `pane_id`, and `worktree` from the returned JSON. If the helper fails, report its error and stop; keep any pane it created available for inspection.
