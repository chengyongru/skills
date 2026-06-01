---
name: pr-fix
description: Use when user wants to checkout someone else's PR, make changes directly as a maintainer, and push to the PR branch
---

# PR Fix

## Overview

Maintainer workflow for directly modifying someone else's PR. Checkout → fix → commit → push. No forks, no branches — push straight to the PR's head branch.

**Prerequisite**: Understand the PR first (`pr-triage`), and know what needs fixing (`pr-review` or user's own assessment).

## When to Use

- User says "fix PR #X" or "push a fix to this PR"
- After `pr-review` found issues that maintainer wants to fix directly
- User wants to commit to someone else's PR branch

## Workflow

### Step 1: Checkout PR

```bash
# Handle dirty working tree first
if ! git diff --quiet; then
  echo "Working tree has uncommitted changes"
  # Ask user: stash or abort?
  git stash push -m "pre-pr-fix-<N>"
fi

gh pr checkout <N>
```

Verify you're on the right branch:

```bash
git log --oneline -5
git branch --show-current
```

### Step 2: Make Changes

Fix the specific issues identified. Follow these rules:

- **Surgical changes only** — fix what was identified, don't refactor adjacent code
- **Match existing style** — follow the PR author's conventions, not your own
- **Keep commits atomic** — one logical fix per commit
- **Don't touch unrelated code** — even if you notice other issues, note them for a comment instead

### Step 3: Commit

```bash
git add <specific files>
git commit -m "$(cat <<'EOF'
fix: <what was fixed and why>

<maintainer edit: brief explanation of what was wrong and how it was fixed>
EOF
)"
```

**Commit message conventions:**
- Use conventional prefix (`fix:`, `style:`, `refactor:`, `test:`)
- Include `maintainer edit` or similar marker so author knows it wasn't them
- Explain WHY, not just WHAT — the diff already shows WHAT

### Step 4: Push

```bash
git push
```

This pushes directly to the PR branch because `gh pr checkout` sets up the tracking branch.

**If push fails** (branch protection, force-push required after rebase):
- Ask user before force-pushing: `git push --force-with-lease`
- Never force-push without user's explicit approval

### Step 5: Verify

After pushing, confirm on GitHub:

```bash
gh pr checks <N>
gh pr view <N> --json commits --jq '.commits | length'
```

## Handling Multiple Fixes

If there are multiple independent issues to fix:

1. Fix and commit each one separately
2. Push after ALL fixes are committed (not after each one)
3. One push = one CI run = faster feedback

```
fix: handle null response from API
fix: add missing error handling in webhook
style: fix inconsistent indentation
```

Then `git push` once.

## Working with the PR Author

- **Leave a comment** explaining what you changed and why, unless the fix is trivial
- **Don't overwrite author's commits** — avoid `git rebase` or `git commit --amend` on commits that aren't yours
- **If you need to rebase** onto target branch, ask author first or let them handle it

```bash
# Comment on the PR after pushing fixes
gh pr comment <N> --body "Pushed a fix for <issue>: <explanation>"
```

## Common Mistakes

| Mistake | Fix |
|--------|-----|
| Modifying without understanding the PR | Run `pr-triage` first |
| Refactoring adjacent code while fixing | Only touch what needs fixing |
| Force-pushing without asking | Always ask first — it rewrites author's history |
| Pushing after each commit | Batch commits, push once |
| Stashing and forgetting to pop | After done: `git stash pop` to restore your work |
| Missing commit context | Always explain WHY in the commit message |
