---
name: pr-review
description: Use when user wants to do a maintainer-quality review of a GitHub PR, identify blockers or recommend rejection/closure, submit COMMENT-only automated GitHub review comments when findings warrant it, or get actionable findings on correctness, architecture, maintainability, focus, tests, and code quality; never approve PRs; use pr-worktree for isolated local checkout before reading or testing PR code
---

# PR Review

## Non-negotiables

- Review only the requested PR.
- If the PR is already merged, skip review and report that it was skipped.
- Use `pr-worktree` for checkout/inspection; never switch the user's current branch.
- Fetch latest `origin/<base>` before judging the PR.
- Do not approve, merge, close, delete branches, force-push, or alter labels/state unless the user explicitly asks for that exact action.
- If GitHub feedback is warranted, this skill authorizes a nanobot automated `COMMENT` review. Never submit `APPROVE`.
- If there are no blockers or useful comments, do not post a GitHub review just to say it is clean.
- Keep the final user report brief unless asked for detail.

## Workflow

### 1. Metadata gate

Run the bundled context helper first:

```bash
python3 <this-skill>/scripts/pr_context.py <N> --repo <OWNER/REPO>
```

Use its output for PR state, mergeability, size, labels, changed files, CI summary, and local-verification guidance.

Stop early when the PR is already merged. For open PRs, infer the behavioral contract from title/body/commits/files/tests before reading code.

### 2. Isolated context

Read `pr-worktree`, create or reuse an isolated worktree, fetch latest base, and inspect the PR from merged/full-repo context.

Read repo-local guidance once when present: `AGENTS.md`, `.agent/design.md`, `.agent/security.md`, `.agent/gotchas.md`, `CONTRIBUTING.md`, nearby package docs.

### 3. Review changed files

Read changed files in context with targeted ranges. Search call sites only when the changed symbol crosses file boundaries or the PR changes shared behavior.

For detailed review criteria, read [references/review-criteria.md](references/review-criteria.md) only when the PR is non-trivial or you need severity calibration.

### 4. Verification decision

Use the CI summary from `scripts/pr_context.py`. Remote CI is the default source of truth for GitHub PRs.

Do not rerun full local CI by default. Read [references/verification.md](references/verification.md) only if the helper reports missing/failing/pending/ambiguous CI or a concrete local reproduction is needed.

### 5. Findings gate before line work

First decide whether there is a real blocker, useful comment, or rejection reason.

- No blocker/useful comment → no inline comments, no GitHub review; report locally.
- Has blocker/useful comment → read [references/line-comments.md](references/line-comments.md), anchor actual file lines, then read [references/github-submission.md](references/github-submission.md) and submit a `COMMENT` review.

Do not confirm inline line numbers during general exploration.

### 6. Final report

Report concisely:

- PR state/mergeability/CI state
- whether blockers or useful comments were found
- whether a GitHub review was posted, with URL if posted
- what was not done: no approve/merge/close/delete/label changes unless explicitly requested

## Anti-loops

- Do not reread this workflow during the same PR review.
- Do not reread the same diff/source range unless the file changed or you are anchoring a concrete finding.
- Do not run full local tests after remote CI is green just to increase confidence.
- Do not expand into unrelated architecture archaeology without a concrete failure hypothesis.
- Do not ask whether COMMENT-only GitHub review posting is allowed; this skill is the authorization.
