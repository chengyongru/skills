---
name: pr-review
description: Perform a maintainer-quality GitHub PR review with actionable findings and merge or closure guidance. Gate deep review on current supported-path reachability and evidenced net value, use pr-worktree for isolation, and publish COMMENT-only feedback when explicitly authorized.
---

# PR Review

Review the requested PR from an isolated checkout. Review is read-only by default; explicit publication may create one `COMMENT` review. Approval, merge, closure, labels, branch changes, and other mutations require their own authorization.

## Prepare

1. Run `scripts/pr_context.py <PR> --repo <OWNER/REPO>` for metadata, mergeability, files, labels, CI, and verification guidance.
2. Prepare/reuse `pr-worktree --mode review`, fetch the latest base and PR head, and read applicable repository instructions.
3. Define purpose, claimed benefit, supported entrypoint/actor, changed contract, expected/actual change cone, maintenance cost, and highest-risk proof obligations.

## Value gate

Trace `supported entrypoint or actor -> current caller -> changed boundary -> concrete consequence`.

- `PASS`: current supported behavior or maintenance burden is reachable and the change has evidenced net value.
- `UNRESOLVED`: inspect the shortest missing contract path.
- `FAIL`: the state is unsupported/unreachable or the benefit is speculative; lead with a close/no-merge recommendation and stop implementation review.

A public API or documented extension contract counts as supported even when consumers are external. Keep merge value separate from implementation correctness. Read `references/review-criteria.md` for non-trivial or cross-boundary PRs.

## Review and verify

1. Inspect changed files from contracts outward. For scope expansion, identify the invariant or consumer that forces each extra file.
2. Classify observations as Confirmed, Risk, Question, or Not a finding. Put reachable, concrete, evidenced issues in findings; keep risks/questions separate.
3. Use CI as configured-matrix evidence. Read `references/verification.md` for missing/ambiguous CI or a focused public, migration, security, race, package, or restart proof.
4. Report findings by impact, then net-value recommendation, risks, questions, and limitations.

## Optional publication

With explicit comment authorization and a useful finding or evidence-backed closure recommendation, read `references/line-comments.md` and `references/github-submission.md`, anchor changed-line comments, and submit one concise `COMMENT` review. Record its URL.

Reply briefly with conclusion/confidence, PR and CI state, purpose and net value, changed contracts/cone, findings, risks/questions, verification, limitations, and any GitHub mutation.
