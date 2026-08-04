---
name: pr-rebase
description: Rebase an existing GitHub PR branch onto the latest base, resolve conflicts while preserving intent, verify the result, and optionally update the remote branch. Use when the user asks to rebase, sync, refresh, or bring a PR up to date.
---

# PR Rebase

A local rebase authorizes fetch and history rewrite in an isolated worktree. Updating the PR branch additionally authorizes `--force-with-lease`; other PR mutations retain separate authorization.

1. Identify PR/base/head repositories and branches, local-only versus remote update, branch writability, and required verification.
2. Prepare or reuse an attached `pr-worktree --mode fix` for the PR head. Preserve unrelated files and confirm the expected tracked branch/upstream.
3. Fetch the base remote and inspect status, recent commits, and the three-dot PR diff.
4. Run `git rebase <base-remote>/<base-branch>`.
5. Resolve conflicts from the current base contract and PR intent: keep current base behavior except where the PR intentionally changes it, reapply the smallest necessary delta, inspect staged resolutions, and run focused checks. Ask the user when a conflict requires a product/ownership decision.
6. After rebase, run status, `git diff --check`, the rebased three-dot diff, and focused contract-driven verification.
7. For an authorized remote update, push `--force-with-lease`; a lease rejection triggers inspection of the new remote head.
8. Read back PR head/base/state and CI after a push.

Use `git rebase --abort` when abandoning the isolated rebase is requested or required. Report old/new heads, conflicts and decisions, verification, remote update, CI, and limitations.
