---
name: pr-fix
description: Use when the user explicitly wants to modify an existing GitHub PR as a maintainer and push focused fixes to its head branch; establish the confirmed issue, protected contract, minimal change cone, and verification evidence first; use pr-worktree so the current workspace is not disturbed
---

# PR Fix

## Non-negotiables

- Use this only when the user explicitly authorizes modifying and pushing to the PR branch.
- Use `pr-worktree` in `fix` mode; never switch or stash the user's current workspace.
- Fix confirmed issues or an explicitly requested change. Do not turn risks/questions into code changes without resolving them.
- Keep the patch inside the minimal causal change cone. Do not bundle cleanup, formatting, or speculative refactors.
- Follow applicable repository instructions and existing contribution/commit conventions.
- Never amend, rebase, rewrite the author's commits, or force-push without explicit approval.
- Do not post comments, reviews, labels, or other PR-state changes unless separately requested or required by repository policy. When labels are authorized, use `pr-label` rather than changing them ad hoc.

## Workflow

### 1. Establish the repair contract

Before editing, write down:

- the confirmed trigger and consequence;
- the violated contract or requested before/after;
- the expected change cone;
- the closest regression or public-surface proof;
- any migration, rollback, or compatibility constraint.

Use `triage` when the PR's purpose is still unclear. Use `pr-review` findings when available, but verify they still match the current head.

### 2. Prepare an isolated fix worktree

Read `pr-worktree` and run its helper:

```bash
python3 <pr-worktree-skill>/scripts/pr_worktree.py prepare <N> --repo <OWNER/REPO> --mode fix --format markdown
```

Use the returned worktree path for every read, edit, test, commit, and push. Verify the manifest reports an attached branch and expected upstream/head repository. If the helper reports a dirty worktree, branch collision, or unwritable fork, stop and report it rather than improvising a destructive checkout.

### 3. Inspect current context

Find and read applicable repository instructions. Compare the current PR against the latest base and confirm the issue has not already changed since review.

Read the narrow owner/call path needed for the repair. Preserve the author's intended design unless that design is the confirmed problem.

### 4. Make the focused change

- Change the smallest surface that enforces the contract.
- Add or update the closest regression test.
- For any file outside the expected cone, record the contract or consumer that forces it to change.
- Preserve unrelated author and user changes.
- Note unrelated defects for later; do not repair them in this push.

### 5. Verify before committing

Run the smallest reliable checks derived from the repair contract:

1. Reproduce the old failure on the base when practical.
2. Run the focused regression on the fixed head.
3. Exercise the public surface, negative path, migration, restart, or concurrency behavior when that is the actual contract.
4. Inspect the final diff for scope drift and accidental generated/lockfile churn.

Do not rely only on the future CI run when a cheap focused proof is available. Do not duplicate a full green matrix without a reason.

### 6. Commit without rewriting author history

Stage specific files and follow the repository's commit conventions. Keep commits logically reviewable and explain why the change is required. Do not force a conventional prefix or maintainer marker when the repository uses another style.

Before committing:

```bash
git branch --show-current
git status --short --branch
git diff --check
git diff --cached
```

### 7. Push normally

```bash
git push
```

The helper prepares the PR head branch and its tracking configuration. Verify the pushed commit appears on the requested PR.

If the contributor fork is not writable, branch protection rejects the push, or history would need rewriting, stop and report the exact blocker. Ask before any `--force-with-lease`; never use plain `--force`.

### 8. Check remote state

After pushing, confirm on GitHub:

```bash
gh pr checks <N> --repo <OWNER/REPO>
gh pr view <N> --repo <OWNER/REPO> --json commits,headRefOid,url
```

Report required checks as passing, failing, or pending. Do not claim success from a push alone.

## Final report

Include:

- confirmed issue and protected contract;
- files and commits added to the PR;
- focused checks and results;
- push result and current CI state;
- remaining risks or verification gaps;
- any extra GitHub mutations performed, or state that none were made.

## Common mistakes

| Mistake | Fix |
|---|---|
| Editing a risk that was never confirmed | Establish trigger, contract, consequence, and evidence first |
| Stashing/switching the current workspace | Use the helper's isolated fix worktree |
| Refactoring adjacent code | Stay inside the causal change cone |
| Pushing from detached HEAD | Require the helper's `mode=fix` attached branch manifest |
| Treating CI as the only proof | Run focused contract-driven verification before push |
| Force-pushing after rejection | Stop and request explicit approval |
| Posting an unsolicited PR comment | Keep publication separate from the authorized code push |
