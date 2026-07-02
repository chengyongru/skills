# Verification Reference

Use this file only when `scripts/pr_context.py` reports missing/failing/pending/ambiguous CI, or when remote CI is otherwise insufficient for the review decision.

## Default

For GitHub PRs, prefer remote CI/checks as the primary verification signal. The repository CI is the source of truth for its configured test matrix.

Do not rerun full local CI when:

- remote CI is present, current for the PR head SHA, and green;
- the changed area is covered by the repository's normal CI matrix;
- no concrete failure hypothesis needs local reproduction.

## When local verification is worth it

Run focused local checks only when at least one condition holds:

- CI is missing, unavailable, stale, pending too long, failed, or ambiguous.
- The PR touches code not covered by CI.
- You found a concrete blocker hypothesis and need reproduction evidence.
- The PR changes behavior that is hard to infer statically.
- The user explicitly asks for local verification.

## Scope

Prefer the smallest reliable check:

1. targeted unit test for the changed module;
2. a tiny black-box/adversarial probe for the claimed invariant;
3. package-specific build/lint when CI is absent or the changed file is build-sensitive;
4. full local suite only when broad shared contracts changed and remote CI cannot answer it.

Do not install dependencies or run long local suites merely to duplicate already-green remote CI.

## Reporting

Mention:

- remote CI state and whether it was trusted;
- any local check you ran and why;
- any verification gap that remains.
