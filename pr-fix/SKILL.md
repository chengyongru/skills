---
name: pr-fix
description: Apply and push a focused maintainer fix to an existing GitHub PR head branch. Use when the user explicitly authorizes modifying that PR. Establish the confirmed issue, protected contract, minimal change cone, and verification evidence; use pr-worktree for isolation.
---

# PR Fix

The user's authorization defines the PR and allowed mutation. Prepare or reuse a matching `pr-worktree --mode fix`; publication, history rewrite, comments, labels, and other PR mutations retain separate authorization.

## Repair cycle

1. Establish the confirmed trigger/consequence, violated contract or requested before/after, expected change cone, closest proof, and compatibility constraints.
2. Prepare the PR fix worktree and confirm its attached branch, upstream, head repository, and existing task-owned changes.
3. Read repository instructions, current base/PR diff, and the narrow owner/caller path.
4. Change the smallest surface enforcing the contract; add or update the closest regression proof. Preserve unrelated author/user work and record why any file outside the expected cone changes.
5. Verify the old failure on base when practical, the focused regression on the fixed head, and the relevant public/negative/migration/restart/concurrency path. Inspect final scope and generated churn.

When invoked by `nanobot-gate`, return the local edits and evidence after step 5. The gate owns resnapshotting, further remediation, and later publication.

## Publish

For directly authorized PR fixes:

1. Stage specific files, inspect the cached diff, and commit with repository conventions while preserving author history.
2. Push normally and confirm the commit on the requested PR.
3. Update title/body only when the final pushed scope made them inaccurate; preserve valid context, links, keywords, templates, and checklists.
4. Read back title/body/head and report required CI as passing, failing, pending, or unavailable.

Use `--force-with-lease` only after explicit history-rewrite approval. Use `pr-label` for authorized labels.

Reply with the repaired contract, changed files/commits, focused evidence, push and CI state, metadata updates, limitations, and every GitHub mutation.
