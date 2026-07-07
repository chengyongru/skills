# Review Criteria Reference

Load this only when the PR is non-trivial, crosses subsystem boundaries, or you need severity calibration.

## Build the maintainer model

Identify only what is relevant to the changed files:

- expected ownership layer
- critical paths
- extension points / canonical helpers
- dependency direction
- compatibility contract
- minimum acceptable diff scope

Do not turn this into repository-wide architecture archaeology.

## Review priority

1. Premise / reachability: does the PR solve a real product or maintainer problem?
2. Security / safety: does it weaken boundaries or allow wrong operations?
3. Correctness: does the implementation satisfy the claimed contract across relevant entrypoints?
4. API compatibility: does it break existing callers/configs/wire contracts?
5. Architecture: does behavior live in the right layer and dependency direction?
6. Tests / CI coverage: are risky paths covered by remote CI or focused tests?
7. Performance: unbounded loops, N+1, leaks, expensive hot-path work.
8. Maintainability / focus: unnecessary churn, broad refactor, needless abstraction.
9. Style only when it affects lint, readability, or maintainability.

## Boundary matrix triggers

Build a small boundary matrix only for changes to validation, parsing, permissions, tool execution, provider adapters, gateways, storage, or other trust boundaries.

Useful dimensions:

- fresh input vs replay/migration
- valid input vs malformed/null/empty/scalar/array
- public API vs internal direct call
- streaming vs non-streaming
- success vs rejected/error path
- telemetry/result fields after failed work

## Severity calibration

- **Reject / close recommendation**: invalid premise, accidental PR, unreachable problem, duplicate/stale work, or complexity not worth carrying.
- **Must fix**: wrong operation could execute, data/security boundary is weakened, public contract breaks, PR's central claim is false, or CI/merge state blocks safe merge.
- **Should fix / useful comment**: likely bug, missing important test, ambiguous API/config semantics, architectural boundary drift, risky complexity, or meaningful residual risk.
- **No blocking findings**: gates pass based on evidence reviewed. This is not approval.

## GitHub comment content

When posting comments, prefer side-effect/risk analysis. Do not include fix suggestions unless the user asked for them or the repository norm requires them.

Use natural English for public GitHub review comments. Avoid labels like `[MINOR]`, `[NIT]`, `[CRITICAL]` in inline comments unless the user explicitly wants that style.
