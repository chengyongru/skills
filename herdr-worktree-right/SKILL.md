---
name: herdr-worktree-right
description: Open the active Git worktree in the pane immediately to the right of the calling Herdr pane, reusing that pane when it exists. Use when the user asks to open the current worktree in a right-hand Herdr pane on Linux or Windows. Requires HERDR_ENV=1.
---

# Herdr Worktree Right

Pass the task's active worktree directory explicitly, rather than the skill directory or an unrelated checkout. Require `HERDR_ENV=1` and inherited `HERDR_PANE_ID`; if absent, report that the calling pane cannot be identified and stop without targeting UI focus.

On Linux, run [scripts/open-worktree-right.py](scripts/open-worktree-right.py) with Python 3 (standard library only; no PowerShell dependency):

```bash
python3 <skill-directory>/scripts/open-worktree-right.py --cwd <active-worktree-path>
```

On Windows, run [scripts/open-worktree-right.ps1](scripts/open-worktree-right.ps1) with PowerShell 7:

```powershell
& <skill-directory>/scripts/open-worktree-right.ps1 -Cwd $PWD.Path
```

The helper resolves the Git worktree and calling pane, reuses the right-hand pane or creates it, and verifies its directory while preserving focus. It leaves an existing pane untouched when changing directories would interrupt a process or the shell prompt cannot be recognized. It creates no worktrees and starts no agents.

Use `--dry-run` on Linux or `-DryRun` on Windows for read-only inspection. Report `status`, `pane_id`, and `worktree` from the returned JSON. If the helper fails, report its error and stop; keep any pane it created available for inspection. Never invent missing caller environment variables.
