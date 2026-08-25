---
name: pr-worktree
description: Maintain one registered Git worktree per branch for PR and topic-branch tasks. Use when locating, creating, reusing, inspecting, or cleaning a branch worktree without disturbing another checkout.
---

# PR Worktree

Use `scripts/pr_worktree.py` as the lifecycle source of truth. Set every later command's `workdir` to the returned path.

## Invariant

- Map each local branch to exactly one registered worktree. Reuse that path across agents and follow-up tasks.
- Resolve a PR to its head branch, then reuse the worktree already carrying that branch. A PR number, task type, or new agent never justifies another worktree.
- Continue in a matching worktree when its existing changes belong to the task. Preserve unrelated changes and stop instead of creating a clean duplicate.
- Keep branch worktrees attached. Do not create detached worktrees; `prepare` may attach a clean legacy PR worktree to its branch.

## Commands

```powershell
python <skill>\scripts\pr_worktree.py start codex/<topic> --repo <OWNER/REPO> --base <base> --format markdown
python <skill>\scripts\pr_worktree.py prepare <PR> --repo <OWNER/REPO> --format markdown
python <skill>\scripts\pr_worktree.py status --path <worktree> --format markdown
```

`start` reuses an already checked-out branch before considering a new path. `prepare` discovers the PR head branch and registered legacy paths before creating the canonical `pr-<number>` path. Read the returned manifest once; do not rediscover or recreate the worktree manually.

## Cleanup

Run cleanup only when requested:

```powershell
python <skill>\scripts\pr_worktree.py cleanup --repo-dir <base-repo> --path <worktree> --format markdown
```

Cleanup preserves worktrees with changes, untracked files, missing upstreams, or unpushed commits. Never force-remove them.
