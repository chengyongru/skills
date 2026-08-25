---
name: pr-fix
description: Apply a focused maintainer fix to an existing GitHub PR head branch. Use when the user authorizes modifying that PR; push only when the remote update is also authorized. Use pr-worktree for isolation.
---

# PR Fix

The user's authorization defines the PR and local edit scope. Prepare or reuse the PR head branch's existing `pr-worktree`; commit, push, and history rewrite retain separate authorization unless the request includes them. This skill owns the focused code fix. After an authorized push, compose `pr-metadata` to synchronize stale title/body; route rebase, labels, review comments, merge, and closure to their own workflows.

## Repair cycle

1. Establish the confirmed trigger/consequence, violated contract or requested before/after, expected change cone, and the smallest proof required by the changed surface.
2. Prepare or reuse the PR head branch worktree and confirm its attached branch, upstream, head repository, and existing task-owned changes.
3. Read repository instructions, current base/PR diff, and the narrow owner/caller path.
4. Change the smallest surface enforcing the contract; add or update the closest regression proof when behavior changed. Preserve unrelated author/user work and record why any file outside the expected cone changes.
5. Choose and run the smallest decisive verification: reproduce a behavioral failure and run its closest regression when practical; add compatibility, authority, persistence, lifecycle, concurrency, packaging, or public-surface proof only when the changed contract requires it. For docs, tests, or config-only changes, use the closest diff/lint/build check. Inspect final scope and generated churn.

When invoked by `nanobot-gate`, return the local edits and evidence after step 5. The gate owns resnapshotting, further remediation, and later publication.

## Publish

Only when commit and push are explicitly authorized:

1. Stage specific files, inspect the cached diff, and commit with repository conventions while preserving author history.
2. Push normally and confirm the commit on the requested PR.
3. Invoke `pr-metadata` to compare the pushed scope with the PR title/body and update stale metadata while preserving valid context.
4. Read back the PR head and report required CI as passing, failing, pending, or unavailable.

Use `--force-with-lease` only after explicit history-rewrite approval. Use `pr-label` for authorized labels.

Reply with the repaired contract, changed files/commits, focused evidence, and only the authorized push, CI, metadata synchronization, and mutation details that apply.
