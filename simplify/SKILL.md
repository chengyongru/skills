---
name: simplify
description: Apply safe, behavior-preserving cleanup to recent or targeted code. Use when the user asks to simplify, reduce duplication or complexity, improve reuse, tighten abstractions, or run a /simplify pass after implementation.
---

# Simplify

Simplify the user-selected target; otherwise use the current diff and recent untracked files. Treat focus text as a constraint on that target.

1. Inspect repository state, relevant code, nearby helpers/tests/callers, and the focused verification command.
2. Review for reuse, avoidable branching or indirection, repeated work, obvious hot-path waste, and misplaced ownership.
3. Apply a change when behavior stays stable, scope stays inside the target, the result fits repository style, and verification is proportionate to risk.
4. Preserve public APIs, schemas, migrations, persistence formats, dependency versions, UX behavior, generated files, and intentional ownership boundaries unless the user includes them in scope.
5. Keep patches focused and reversible; update tests only as needed by the cleanup.
6. Run the narrowest relevant verification and report changed simplifications, verification, and any higher-risk ideas left untouched.

If the target is unclear outside a repository, ask for the path or scope.
