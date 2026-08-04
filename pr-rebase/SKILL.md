---
name: pr-rebase
description: Safely rebase an existing GitHub pull request branch onto the latest base branch, resolve conflicts while preserving the PR's intent, rerun focused verification, and optionally update the remote PR branch. Use when the user asks to rebase, sync, refresh, or bring a PR up to date with main or another base branch, especially before merge or after the base branch changed.
---

# PR Rebase

Rebase is a history-rewriting operation. Isolate it from the user's current workspace, make the base and head explicit, preserve the PR's change contract through conflicts, verify the rebased result, and only rewrite the remote branch when the user authorized updating the PR.

## Authorization boundary

- A request to rebase locally authorizes fetching and rewriting the isolated local PR branch, but does not authorize pushing it.
- A request to rebase the PR onto a base and update the PR authorizes the required `--force-with-lease` push to that PR head branch.
- Never use plain `--force`.
- Do not merge, close, approve, label, comment on, or request review for the PR unless separately requested.
- Do not rebase a contributor's branch or rewrite another author's history without explicit authorization from the user who controls that workflow.

## Relationship to the PR skills

- Use `pr-worktree` first for PR checkout, branch ownership, and isolation. Reuse the current
  worktree when it is already the requested PR's attached head branch and the rebase belongs to that
  worktree; prepare another worktree only when the current one does not match or contains unrelated
  work.
- Use `pr-review` when the user wants a review or merge recommendation; do not turn rebase into a review.
- Use `pr-fix` when the user also requests code changes to fix a PR. `pr-rebase` owns the history synchronization step and its verification.
- Use `pr-label` only when label changes are explicitly requested.

## Workflow

### 1. Establish the rebase contract

Identify:

- PR number or URL, repository, head repository/branch, and base repository/branch;
- whether the request is local-only or includes updating the remote PR;
- the current PR state and whether the head branch is writable;
- the verification commands required by the repository and the PR's changed surfaces.

If the PR is merged or closed, do not rewrite its branch. Report the state and stop unless the user explicitly asks for a separate branch operation.

### 2. Prepare an isolated worktree

Read and follow `pr-worktree`. If a matching attached PR worktree is already current, continue there.
Otherwise prefer its deterministic helper in fix mode because the branch will be rewritten and possibly
pushed:

```bash
python3 <pr-worktree-skill>/scripts/pr_worktree.py prepare <PR> --repo <OWNER/REPO> --mode fix --format markdown
```

Use the returned worktree path for every command. Confirm the manifest reports an attached, tracked-clean branch, the expected PR head, and a writable upstream. Preserve untracked files; never stash, reset, checkout over, or delete unrelated user work.

### 3. Fetch and inspect the base

From the isolated worktree:

```bash
git fetch <base-remote> <base-branch>
git status --short --branch
git log --oneline --decorate -5
git diff --stat <base-remote>/<base-branch>...HEAD
```

Use the fetched remote-tracking base as the rebase target. Do not rebase onto a stale local `main`.

### 4. Rebase and resolve conflicts

Run:

```bash
git rebase <base-remote>/<base-branch>
```

If conflicts occur:

1. Read the conflict in the context of both the current base and the PR's intended contract.
2. Preserve the latest base behavior unless the PR explicitly changes that behavior.
3. Reapply only the PR's necessary delta; do not retain deprecated code merely because it was in the old PR.
4. Check all conflict markers and inspect the staged diff.
5. Run focused tests for each conflicted surface before continuing when practical.
6. Stage resolved files and continue with `git rebase --continue`.

If the conflict exposes an unclear product or ownership decision, stop the rebase and ask the user. Use `git rebase --abort` only when abandoning the operation is requested or clearly required; report that it restores the isolated worktree to its pre-rebase state.

### 5. Verify the rebased head

After rebase:

```bash
git status --short --branch
git diff --check
git diff --stat <base-remote>/<base-branch>...HEAD
```

Run the smallest reliable verification required by the changed contract, including focused tests and lint. Compare the resulting diff against the pre-rebase PR intent. Do not claim the PR is ready solely because rebase completed.

### 6. Update the remote only when authorized

If the user authorized updating the PR and verification passes, push with lease protection:

```bash
git push --force-with-lease <head-remote> <head-branch>
```

If the lease rejects because the remote changed, stop and inspect the new remote head. Do not overwrite concurrent work or fall back to plain `--force`.

If the user requested only a local rebase, stop before pushing and report the rebased worktree and commit.

### 7. Confirm remote PR state

When the branch was pushed, verify the PR points at the new head:

```bash
gh pr view <PR> --repo <OWNER/REPO> --json state,baseRefName,headRefName,headRefOid,url
gh pr checks <PR> --repo <OWNER/REPO>
```

Report checks as passing, failing, pending, or unavailable. Rebase success is distinct from CI success.

## Failure handling

- Dirty tracked worktree: stop and preserve it; do not stash or reset.
- Missing or stale PR head/base: fetch and verify repository/branch identity before acting.
- Unwritable contributor fork: report the exact push failure and stop.
- Conflict with unclear intent: stop and ask; do not guess.
- Rebase completed but verification fails: do not push unless the user explicitly accepts the failing evidence.
- Remote changed during rebase: inspect and require a fresh lease-safe decision.

## Final report

Include:

- PR URL and base/head branches;
- old and new head commits;
- conflicts resolved and any meaningful decisions;
- verification commands and results;
- whether the remote branch was updated and the current PR/CI state;
- remaining limitations or follow-up needed.
