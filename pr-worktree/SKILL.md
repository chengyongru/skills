---
name: pr-worktree
description: Use when any GitHub PR workflow needs to checkout, inspect, review, test, or modify a PR locally without disturbing the current workspace; provides isolated git worktree checkout and cleanup conventions for triage, pr-review, and pr-fix
---

# PR Worktree

## Overview

Checkout GitHub PRs into isolated git worktrees so PR triage, review, tests, and maintainer fixes never switch branches or pollute the user's current workspace.

Use this skill before any `gh pr checkout`-style operation in `triage` PR mode, `pr-review`, or `pr-fix`.

## Workflow

### Step 1: Resolve PR Metadata

Get the PR number, repo, base, and head first:

```bash
gh pr view <N-or-url> --json number,headRefName,baseRefName,headRepositoryOwner,headRepository,author
```

If the user gave a URL, include `--repo <OWNER/REPO>` in later `gh` commands when needed.

### Step 2: Create an Isolated Worktree

Do not run `gh pr checkout` in the current workspace. Create a sibling/temp worktree, or use a local `.worktrees/` directory only when it is already ignored or established in the repo.

Recommended path:

```bash
git check-ignore -q .worktrees/ && WT=.worktrees/pr-<N> || WT=../<repo-name>-pr-<N>
git fetch origin pull/<N>/head:refs/remotes/origin/pr/<N>
git worktree add "$WT" refs/remotes/origin/pr/<N>
```

If the worktree already exists, reuse it after checking its status:

```bash
git -C "$WT" status --short
git fetch origin pull/<N>/head:refs/remotes/origin/pr/<N>
git -C "$WT" checkout --detach refs/remotes/origin/pr/<N>
```

If the repo uses a different remote name, detect it with `git remote -v` and substitute that remote.

### Step 3: Work From the Worktree

Run reads, diffs, tests, and build commands with `workdir` set to the PR worktree path.

For diffs, compare against the remote base:

```bash
git -C "$WT" fetch origin <base-ref>
git -C "$WT" diff origin/<base-ref>...HEAD
```

Keep the user's original workspace branch unchanged.

### Maintainer Fixes

When the task requires pushing to the PR branch, use the PR author's actual head branch and tracking remote.

Prefer `gh pr checkout <N>` only inside the isolated worktree:

```bash
git worktree add "$WT_FIX" HEAD
gh pr checkout <N>
```

Run both commands with `workdir` set appropriately so only the isolated worktree changes branch. Verify the tracking branch before committing:

```bash
git branch --show-current
git status --short --branch
git remote -v
```

Never force-push without explicit user approval.

### Cleanup

Do not automatically delete the worktree at the end of triage/review; keeping it allows follow-up `pr-review` or `pr-fix` work. If the user asks to clean up:

```bash
git worktree remove "$WT"
git worktree prune
```

If the worktree has local changes, ask before removing it.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Running `gh pr checkout` in the user's current workspace | Create/use a PR worktree first |
| Diffing against a stale local base branch | Fetch and diff against `origin/<base-ref>` |
| Removing the worktree after triage automatically | Keep it for follow-up unless user asks |
| Pushing from a detached review worktree | For fixes, checkout the real PR head branch inside the isolated worktree |
