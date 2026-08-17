---
name: pr-worktree
description: Prepare and manage isolated worktrees for GitHub PR workflows that need local checkout, testing, editing, or history changes. Use for implementation, review, testing, fixes, rebase, or cleanup; remote-only triage and label operations do not need a worktree.
---

# PR Worktree

Use `scripts/pr_worktree.py` as the lifecycle source of truth and set every later command's `workdir` to its returned path.

## Choose the path

- Reuse the current worktree when its repository, branch/HEAD, and changes belong to the task.
- New PR: create or reuse an attached topic branch with `start`.
- Existing PR read/test/review: use `prepare --mode review`, which checks out the PR branch with `gh pr checkout` in the isolated worktree.
- Existing PR authorized edits/rebase: use attached `prepare --mode fix` on the PR head branch.

```powershell
python <skill>\scripts\pr_worktree.py start codex/<topic> --repo <OWNER/REPO> --base <base> --format markdown
python <skill>\scripts\pr_worktree.py prepare <PR> --repo <OWNER/REPO> --mode review --format markdown
python <skill>\scripts\pr_worktree.py prepare <PR> --repo <OWNER/REPO> --mode fix --format markdown
python <skill>\scripts\pr_worktree.py status --path <worktree> --format markdown
```

The manifest provides repository/ref identity, selected remote, worktree path, attached/detached state, cleanliness, upstream, PR-head relation, and ready commands. Read it once.

When a review already has JSON metadata from `pr_context.py`, pass it with `--context-json` so the helper does not reread the same PR metadata.

## Safety contract

- Preserve the user's current workspace and unrelated tracked/untracked files.
- Accept review or fix reuse only when clean and attached to the intended PR head branch.
- Treat locally ahead fix branches as intentional maintainer work; resolve behind/diverged state before editing.
- Let `start` attach a safe existing local branch or create a new branch from the fetched base. Use `--source head` only for a clean committed local starting point.
- Use normal pushes for new/fix branches. Force operations and PR creation require their own explicit authorization.
- Keep prepared worktrees for follow-up.

## Cleanup

Run cleanup only when requested:

```powershell
python <skill>\scripts\pr_worktree.py cleanup --repo-dir <base-repo> --path <worktree> --format markdown
```

The helper preserves paths with tracked changes, untracked files, missing upstreams, or unpushed commits and reports the exact blocker. Use the reported state to choose the next action.
