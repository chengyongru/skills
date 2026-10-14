# Comment and workaround cleanup

Treat comments as claims to verify. Prefer code that makes internal behavior apparent and checks that enforce its constraints.

## Scope and review

1. Inherit the caller's files or diff. For an explicitly requested repository audit, cover owned source modules; exclude generated and vendored code. State coverage and omissions.
2. For a broad audit, use independent read-only subagents over disjoint modules when delegation is available and authorized; otherwise inspect sequentially. Give each worker the scope and this reference. Workers return findings and evidence; the coordinator owns all edits and spot-checks findings against source.
3. Read each candidate beside its symbol, callers, and closest proof. Check external claims against the pinned dependency, platform behavior, or durable issue/specification. A comment's own claim is not proof.
4. Classify each candidate using the table below. Prioritize recurring workaround patterns and reader burden; deletion count is an inventory, not a success metric.

| Decision | Evidence and action |
|---|---|
| Delete | Code restatement, task narration, redundant banners, stale claims, or abandoned commented-out code with no remaining contract. Remove the prose after checking its syntactic and tooling role. |
| Refactor | An explanation compensates for internal naming, ownership, control flow, invalid states, or a workaround. Name the reachable trigger, affected symbol, intended contract, and smallest structure that removes the need for the explanation. |
| Keep | Required legal text, active tool directives, public API documentation, or a verified external dependency/platform/protocol constraint that code cannot make apparent. Preserve the non-obvious fact and its durable source. |
| Unresolved | The constraint, consumer, tool effect, or external prerequisite cannot be established. Retain it, name the missing evidence, and propose the cheapest way to resolve it. |

Inspect suppressions against their actual rule and affected code. A suppression of a real correctness problem is a refactor candidate; remove it together with the proven fix. Required shebangs, encoding declarations, build directives, type/lint pragmas, and formatter controls have tool effects even when they look like prose.

Treat docstrings and documentation comments that define behavior or generate public documentation as contracts. Read strings, examples, and test fixtures as data unless their role is established. Use syntax-aware edits; regex matches locate candidates, not safe deletion ranges.

## Plan or apply

- For audit/plan requests, keep the parent and every worker read-only. Return a grouped high-level plan: direct deletions, root-cause refactors, justified keeps, and unresolved claims. Give representative `file:line` locations, affected symbols, evidence, expected benefit, and proposed verification; avoid an exhaustive comment dump.
- For cleanup requests, apply confirmed direct deletions and behavior-preserving refactors within the requested scope. Keep a workaround's explanation until its replacement enforces the same contract; then remove both together. Report broader API, schema, dependency, or product changes as separate proposals.
- Encode internal constraints with clear ownership, domain types, boundary checks, or the closest meaningful regression proof. Verify the claimed failure path before replacing prose with enforcement.
- Check parsing and relevant lint/build rules after ordinary deletions. Changes to directives, documentation contracts, or workaround behavior need their corresponding tool, consumer, or behavioral proof. Use `verify` or the matching project verifier when a public path changes.
- Report the plan or applied changes, verification actually run, retained constraints, unresolved work, and coverage directly in the conversation. Keep raw evidence only when it supports reproduction.
