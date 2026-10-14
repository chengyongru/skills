---
name: simplify
description: Apply behavior-preserving cleanup to recent or targeted code, including redundant comments and workaround structure. Use for simplify requests, duplication or complexity reduction, comment pruning, or a comment/workaround audit with a high-level plan.
---

# Simplify

Simplify the user-selected target; otherwise use the current diff and recent untracked files. Treat focus text as a constraint on that target.

For an audit or plan-only request, inspect and report without editing. Use repository-wide scope only when requested.

1. Inspect repository state, relevant code, nearby helpers/tests/callers, and the focused verification command.
2. Review for reuse, avoidable branching or indirection, repeated work, obvious hot-path waste, and misplaced ownership. For comment cleanup or scoped comments explaining workarounds, suppressions, or invariants, read [references/comment-cleanup.md](references/comment-cleanup.md).
3. In cleanup mode, apply a change when behavior stays stable, scope stays inside the target, the result fits repository style, and verification is proportionate to risk.
4. Preserve public APIs, schemas, migrations, persistence formats, dependency versions, UX behavior, generated files, and intentional ownership boundaries unless the user includes them in scope.
5. Keep patches focused and reversible; update tests only as needed by the cleanup.
6. In tests, assert the intended result positively. Do not use negative assertions against old text, symbols, or implementation details merely to prove removal.
7. In cleanup mode, run the narrowest relevant verification and report changed simplifications, verification, and any higher-risk ideas left untouched. In audit mode, return a high-level plan with evidence and the checks each proposed change would need.

If the target is unclear outside a repository, ask for the path or scope.
