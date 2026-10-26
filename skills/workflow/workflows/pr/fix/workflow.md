# PR Fix

The user's authorization defines the PR and local edit scope. Prepare or reuse the PR head branch's existing [pr-worktree](../worktree/workflow.md); commit, push, and history rewrite retain separate authorization unless the request includes them. This skill owns the focused code fix. After an authorized push, compose [pr-metadata](../metadata/workflow.md) to synchronize stale title/body; route rebase, labels, review comments, merge, and closure to their own workflows.

## Repair cycle

1. Establish the confirmed trigger/consequence, violated contract or requested before/after, expected change cone, and the smallest proof required by the changed surface.
2. Prepare or reuse the PR head branch worktree and confirm its attached branch, upstream, head repository, and existing task-owned changes.
3. Read repository instructions, current base/PR diff, and the narrow owner/caller path. When a behavioral root cause is unclear, reproduce it on the affected surface, list plausible mechanisms, and use targeted observations to eliminate candidates before editing. Keep only fixes supported by a surviving cause; discard changes motivated by disproven hypotheses.
4. Change the smallest surface enforcing the contract; add or update the closest regression proof when behavior changed. Preserve unrelated author/user work and record why any file outside the expected cone changes.
5. Choose and run the smallest decisive verification: reproduce a behavioral failure and run its closest regression when practical; add compatibility, authority, persistence, lifecycle, concurrency, packaging, or public-surface proof only when the changed contract requires it. For docs, tests, or config-only changes, use the closest diff/lint/build check. Inspect final scope and generated churn.

## Publish

Only when commit and push are explicitly authorized:

1. Stage specific files, inspect the cached diff, and commit with repository conventions while preserving author history.
2. Push normally and confirm the commit on the requested PR.
3. Invoke [pr-metadata](../metadata/workflow.md) to compare the pushed scope with the PR title/body and update stale metadata while preserving valid context.
4. Read back the PR head and report required CI as passing, failing, pending, or unavailable.

Use `--force-with-lease` only after explicit history-rewrite approval. Use [pr-label](../labels/workflow.md) for authorized labels.

Reply with the repaired contract, changed files/commits, focused evidence, and only the authorized push, CI, metadata synchronization, and mutation details that apply.
