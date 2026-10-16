# Simplify

Simplify the user-selected target; otherwise use the current diff and recent untracked files. Treat focus text as a constraint on that target.

For an audit or plan-only request, inspect and report without editing. Use repository-wide scope only when requested.

1. Inspect repository state, relevant code, nearby helpers/tests/callers, and the focused verification command.
2. Review for reuse, avoidable branching or indirection, repeated work, obvious hot-path waste, and misplaced ownership. For comment cleanup or scoped comments explaining workarounds, suppressions, or invariants, read [references/comment-cleanup.md](references/comment-cleanup.md).
3. In cleanup mode, apply a change when behavior stays stable, scope stays inside the target, the result fits repository style, and verification is proportionate to risk.
4. Preserve public APIs, schemas, migrations, persistence formats, dependency versions, UX behavior, generated files, and intentional ownership boundaries unless the user includes them in scope.
5. Keep patches focused and reversible; update tests only as needed by the cleanup.
6. In tests, prove the intended behavior with positive assertions on observable results, roles, content, or state. Do not add vacuous negative assertions: absence of removed wording, obsolete symbols, unused branches, or things the scenario never introduced is not evidence of correctness. A negative assertion is justified only by a concrete reachable failure, with setup that exercises that risk (for example, seed private data before checking isolation). Ask what incorrect behavior would make each assertion fail; remove assertions with no meaningful answer.
7. In cleanup mode, run the narrowest relevant verification and report changed simplifications, verification, and any higher-risk ideas left untouched. In audit mode, return a high-level plan with evidence and the checks each proposed change would need.

For a specifically requested fresh comment-review lens, read the [comment method](methods/comments.md). Use the existing comment-cleanup reference for the normal audit; do not run both processes by default. The parent retains edit and verification ownership.

If the target is unclear outside a repository, ask for the path or scope.
