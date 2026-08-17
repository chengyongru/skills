---
name: pr-review
description: Perform a maintainer-quality GitHub PR review with actionable findings and merge or closure guidance. Use pr-worktree for isolation, apply reachability and net-value gates to non-trivial reviews, and publish only the explicitly authorized review event.
---

# PR Review

Review the requested PR from an isolated checkout. Review is read-only by default; explicit publication may create one authorized `COMMENT` or `REQUEST_CHANGES` review. Approval, merge, closure, labels, branch changes, and other mutations require their own authorization.

## Prepare

1. Classify the review as focused or deep. Focused reviews inspect the changed contract and closest proof. Deep reviews define purpose, claimed benefit, supported entrypoint/actor, expected/actual change cone, maintenance cost, and highest-risk proof obligations.
2. For a deep review, run `scripts/pr_context.py <PR> --repo <OWNER/REPO> --format json` once and pass its JSON output to `pr-worktree prepare --context-json`. Skip the context helper when CI, mergeability, labels, and a file summary cannot change a focused decision.
3. Prepare/reuse `pr-worktree --mode review`, use its manifest for the PR head, base ref, and checkout state, and read applicable repository instructions. The helper reuses the context JSON when supplied instead of calling `gh pr view` again.

## Value gate for deep reviews

Use this gate for cross-boundary, security/data, lifecycle, high-maintenance, or premise-sensitive PRs. Trace `supported entrypoint or actor -> current caller -> changed boundary -> concrete consequence`.

- `PASS`: current supported behavior or maintenance burden is reachable and the change has evidenced net value.
- `UNRESOLVED`: inspect the shortest missing contract path.
- `FAIL`: the state is unsupported/unreachable or the benefit is speculative; lead with a close/no-merge recommendation and stop implementation review. Do not apply this gate to a focused docs, test, config, or isolated code review unless its premise is itself in question.

A public API or documented extension contract counts as supported even when consumers are external. Keep merge value separate from implementation correctness. Read `references/review-criteria.md` for non-trivial or cross-boundary PRs.

## Review and verify

1. Inspect changed files from contracts outward. For a focused review, avoid a full value packet and inspect only the changed contract and closest consumer or test. For scope expansion, identify the invariant or consumer that forces each extra file.
2. Classify observations as Confirmed, Risk, Question, or Not a finding. Put reachable, concrete, evidenced issues in findings; keep risks/questions separate.
3. Use CI as configured-matrix evidence and choose the smallest decisive proof for the changed surface. Read `references/verification.md` when CI is missing/ambiguous or the surface needs focused public, migration, security, race, package, or restart proof.
4. Report only decision-relevant findings, risks/questions, verification, and limitations. Add the net-value recommendation for deep reviews or when the user asks for merge guidance.

## Optional publication

With explicit publication authorization and a useful finding or evidence-backed closure recommendation, read `references/line-comments.md` and `references/github-submission.md`, anchor changed-line comments, and submit one concise review using the exact authorized event. Never substitute `COMMENT` for an explicitly requested `REQUEST_CHANGES` event. Record its URL.

Reply briefly with the conclusion, changed contract, findings, focused verification, limitations, and any GitHub mutation. Include CI, value, or change-cone details when they affect the decision.
