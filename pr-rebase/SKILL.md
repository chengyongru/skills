---
name: pr-rebase
description: Rebase an existing GitHub PR branch onto the latest base, resolve conflicts while preserving intent, verify the result, and optionally update the remote branch. Use when the user asks to rebase, sync, refresh, or bring a PR up to date.
---

# PR Rebase

A local rebase authorizes fetch and history rewrite in the branch worktree. Updating the PR branch additionally authorizes `--force-with-lease`. This skill rebases, resolves rebase conflicts, verifies the rebased branch, and optionally pushes it; it does not fix unrelated defects or change PR metadata, labels, comments, merge, or closure state.

1. Identify PR/base/head repositories and branches, local-only versus remote update, branch writability, and required verification.
2. Prepare or reuse the PR head branch's existing attached `pr-worktree`. Preserve unrelated files and confirm the expected tracked branch/upstream.
3. Use the manifest's fetched `baseTrackingRef` and inspect status, recent commits, and the three-dot PR diff. Fetch again only when the manifest is unavailable or stale.
4. Run `git rebase <base-remote>/<base-branch>`.
5. Resolve conflicts from the current base contract and PR intent: keep current base behavior except where the PR intentionally changes it, reapply the smallest necessary delta, inspect staged resolutions, and run focused checks. Ask the user when a conflict requires a product/ownership decision.
6. After rebase, run status, `git diff --check`, the rebased three-dot diff, and focused contract-driven verification.
7. For an authorized remote update, push `--force-with-lease`; a lease rejection triggers inspection of the new remote head.
8. Read back the PR head/base after a push and confirm the requested branch now points to the rebased head.

Use `git rebase --abort` when abandoning the rebase is requested or required. Report old/new heads, conflicts and decisions, focused verification, remote update, and limitations.
