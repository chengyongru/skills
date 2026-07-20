---
name: pr-review
description: Use when the user wants a maintainer-quality review of a GitHub PR, actionable findings, blocker or closure recommendations, or explicitly authorized COMMENT-only GitHub feedback; evaluate purpose, expected benefit, scope, contracts, ownership, evidence, and long-term maintenance cost; never approve PRs; use pr-worktree for isolated local checkout before reading or testing PR code
---

# PR Review

## Non-negotiables

- Review only the requested PR.
- Use `pr-worktree` for checkout/inspection; never switch the user's current branch.
- Fetch the PR head and latest remote base before judging the diff.
- Do not approve, merge, close, delete branches, force-push, or alter PR state.
- Treat review and publication as separate actions. Do not post reviews, comments, or labels unless the user explicitly requests it or applicable repository policy explicitly authorizes it.
- If publication is authorized, submit `COMMENT` only. Never submit `APPROVE`; use `REQUEST_CHANGES` only when the user explicitly asks for that event.
- A smell is a hypothesis, not a finding. Require a reachable path, concrete impact, and code/test/contract evidence.
- Green CI is evidence for the configured matrix, not proof that every changed contract is safe.
- A PR can be correct and still not be worth merging. Keep correctness findings separate from the net-value recommendation.
- Use the user's language for the local report. Follow repository norms or the PR discussion language for public comments.
- Keep the final user report brief unless asked for detail.

## Workflow

### 1. Metadata gate

Run the bundled context helper first:

```bash
python3 <this-skill>/scripts/pr_context.py <N> --repo <OWNER/REPO>
```

Use its output for PR state, mergeability, size, labels, changed files, CI summary, and local-verification guidance.

If the PR is merged, state that clearly and keep the review retrospective/read-only. Do not attempt GitHub review submission on a merged PR.

### 2. Isolated context

Read `pr-worktree`, run its helper to create or reuse an isolated review worktree, and inspect the PR from merged/full-repository context.

Find and read applicable repository-local instructions, including hierarchical `AGENTS.md`, contribution rules, design/security docs, and package-local guidance. Do not hardcode one repository's filenames as universal policy.

### 3. Build the review contract before deep code reading

Write a compact review packet from the PR body, commits, changed files, nearby tests, and repository guidance:

- **Purpose and benefit**: what useful outcome the PR buys, who benefits, what happens if it is not merged, and which evidence supports the claimed value.
- **Scope**: the problem, user-visible before/after, and explicit non-goals.
- **Contracts**: public, persisted, security, concurrency, lifecycle, or model-visible behavior that may change.
- **Expected change cone**: the owner module, nearest shared seam, closest tests, and required docs/config/migration.
- **Actual change cone**: every changed area outside the expectation and its claimed causal reason.
- **Maintenance tradeoff**: complexity removed versus concepts, branches, dependencies, ownership burden, blast radius, and recurring proof obligations added.
- **Net value**: whether the evidenced benefit justifies the long-term carrying cost, or whether a smaller change, separate PR, or closure is preferable.
- **Proof obligations**: evidence required for the highest-risk contract.

Answer these two questions explicitly in plain language before deep implementation review:

1. What is this PR for, and what material benefit would merging it provide?
2. What are its long-term maintenance advantages and disadvantages, and is the benefit worth that cost?

Do not repeat the PR author's claims as conclusions. Distinguish claimed benefit from evidence-backed benefit and identify missing product, user, operational, or maintenance evidence.

If the central behavior cannot be explained from artifacts, report that uncertainty before speculating about implementation details.

For non-trivial or cross-boundary PRs, read [references/review-criteria.md](references/review-criteria.md).

### 4. Inspect from contracts outward

Read changed files in context with targeted ranges. Trace callers, consumers, state transitions, or persisted/wire formats only when needed to verify a contract.

For every file outside the expected change cone, ask:

1. Which invariant or consumer forces this file to change?
2. What fails if it is left unchanged?
3. Is the change required behavior, or bundled cleanup/formatting/abstraction?

Unrelated cleanup is a scope finding even when the code is locally correct.

### 5. Verification decision

Use the CI summary from `scripts/pr_context.py` as the baseline signal for the repository's configured matrix.

Compare CI coverage with the proof obligations. Do not rerun full local CI merely to duplicate a green matrix, but do not let green CI hide an uncovered public surface, migration, security boundary, race, package consumer, or restart path.

Read [references/verification.md](references/verification.md) when CI is missing/failing/pending/ambiguous or when a focused reproduction, negative test, public-surface smoke test, migration check, or black-box validation is needed.

### 6. Findings gate before line work

Classify observations before writing comments:

- **Confirmed**: reachable, concrete impact, supported by code/test/contract evidence.
- **Risk**: plausible but missing a threat model, reproduction, or contract fact.
- **Question**: intent or ownership is unclear.
- **Not a finding**: existing behavior, tests, or external contracts resolve the concern.

Only confirmed blockers and useful confirmed findings belong in the findings list. Report material risks or questions separately without presenting them as defects.

Keep merge-value judgments separate from correctness findings. A technically correct PR whose evidenced benefit does not justify its maintenance cost may warrant a simplify, split, or close recommendation, but explain the tradeoff instead of inventing a code defect.

Do not confirm inline line numbers during general exploration.

### 7. Optional GitHub submission

Only when publication is authorized and at least one useful finding exists:

1. Read [references/line-comments.md](references/line-comments.md) and anchor concrete findings to changed lines when possible.
2. Read [references/github-submission.md](references/github-submission.md).
3. Submit one concise `COMMENT` review and record its URL.

Do not post a clean-review comment merely to create activity. Apply labels only when the user or repository policy requests them. Use `pr-label` for policy discovery, planning, mutation, and verification rather than embedding a label taxonomy here.

### 8. Final report

Report concisely:

- conclusion and review confidence
- PR state, mergeability, and CI state
- purpose, evidence-backed benefit, expected/actual change cone, and changed contracts
- long-term maintenance advantages/disadvantages and the net-value assessment
- confirmed findings ordered by impact
- material risks, questions, and evidence gaps
- focused verification performed and limitations
- any GitHub mutations performed, with URLs; otherwise state that the review remained local/read-only

## Anti-loops

- Do not reread this workflow during the same PR review.
- Do not reread the same diff/source range unless the file changed or you are anchoring a concrete finding.
- Do not run full local tests after remote CI is green merely to increase confidence.
- Do not expand into unrelated architecture archaeology without a contract or failure hypothesis.
- Do not convert every uncertainty into a comment; resolve it or label it as a risk/question.
- Do not let file count, unfamiliarity, or stylistic dislike substitute for a causal scope argument.
