# Review Criteria Reference

Load this only when the PR is non-trivial, crosses subsystem boundaries, or needs severity calibration.

## SCOPE model

Use five questions to keep the review decision-focused:

1. **Scope** — Should this behavior exist? State the problem, affected user, before/after, and non-goals.
2. **Contracts** — Which public, persisted, security, concurrency, lifecycle, or model-visible promises may change?
3. **Ownership** — Which layer owns the behavior, and which extension seam should carry it?
4. **Proof** — What reproduction and verification demonstrate the claim and protect the risky paths?
5. **Entropy** — What concepts, dependencies, migration burden, or future maintenance cost does the PR add?

A PR is not safe because these dimensions average out. A single failed security, data, or compatibility obligation can block the change.

## Build the expected change cone

Before deep code reading, predict the smallest justified footprint:

```text
problem → owner module → shared seam/consumer → closest tests → required docs/config/migration
```

Compare it with the actual changed files. For every file outside the expected cone, require a causal explanation supported by at least one of:

- a call path or consumer that must adapt;
- a contract or persisted/wire format that changes;
- a test that would otherwise fail;
- a required migration, compatibility shim, or user-facing document.

Bundled cleanup, formatting, speculative abstraction, or unrelated modernization is scope drift even when locally correct. A large diff may still be justified when every cross-layer edge is causal; file count alone is not a finding.

## Risk axes

Assess each axis and take the highest result rather than an average:

- **Boundary depth / blast radius** — leaf implementation, shared seam, core transaction, or trust boundary.
- **External or persisted contract** — API, CLI, config, wire format, plugin schema, database/file format, cached state.
- **Authority / security** — authentication, authorization, filesystem, process execution, network, secrets, tenant/session isolation.
- **Irreversibility / migration** — deletion, overwrite, schema evolution, backfill, rollback, user data.
- **Concurrency / lifecycle** — retries, cancellation, timeouts, ordering, idempotency, partial completion, restart recovery.
- **Evidence gap** — behavior outside CI, unsupported platform, mocked external integration, browser/package/runtime-only surface.

Changes to authority, irreversible data, core transactions, or concurrent side effects require the deepest review even when isolated to one file.

## Contract inventory

Treat a surface as a contract when external code, stored user state, or another subsystem relies on it. Do not use naming conventions such as a leading underscore as the only test.

Common contracts:

- request/response shapes and error semantics;
- config aliases, defaults, parse/dump behavior, and migration;
- CLI flags, stdout/stderr, exit codes, signals, and environment behavior;
- event ordering, streaming, retries, deduplication, and idempotency;
- persisted records, replay, compaction, atomicity, and recovery;
- plugin discovery, schemas, names, collision rules, and lazy loading;
- prompt templates, tool descriptions, model-visible history, and sanitized context;
- package exports, build artifacts, optional dependencies, and old import paths.

## Proof obligations by surface

| Changed surface | Minimum useful evidence |
|---|---|
| Leaf adapter/integration | focused unit tests, error/lifecycle path, optional dependency or discovery behavior |
| Public API/config/CLI/wire | old-caller fixture or compatibility check, round trip, malformed/error cases, public-interface smoke |
| Persistent state/migration | old data fixture, restart/replay, duplicate handling, atomicity, upgrade/rollback story |
| Security/authority | deny-first negative matrix, bypass attempts, parent/child capability monotonicity, secret-safe logging |
| Concurrency/retry/cancel | ordering, partial completion, duplicate side effects, cancellation propagation, timeout/restart |
| UI/user workflow | state tests plus real public-surface interaction when browser/runtime behavior matters |
| Packaging/dependencies | clean build/install/import or consumer smoke in the supported environment |
| Model-visible behavior | deterministic contract/snapshot tests where possible and an explicit limitation when model evaluation is required |

## Finding standard

An observation becomes a finding only when the review can state:

1. the reachable trigger or affected caller;
2. the violated contract or incorrect behavior;
3. the concrete consequence;
4. the evidence in code, tests, reproduction, or authoritative docs.

Classify everything else explicitly:

- **Confirmed** — all four elements are present.
- **Risk** — plausible consequence, but one or more proof elements are missing.
- **Question** — intent, scope, or ownership needs clarification.
- **Not a finding** — evidence resolves the concern or it is only preference.

Do not launder uncertainty into severity through persuasive wording.

## Review priority

1. Premise and reachability.
2. Security, authority, and data safety.
3. Correctness across affected entrypoints and lifecycle states.
4. Compatibility and migration.
5. Ownership and dependency direction.
6. Proof coverage and residual gaps.
7. Performance and resource bounds.
8. Maintainability, focus, and unnecessary entropy.
9. Style only when it affects correctness, tooling, or sustained readability.

## Severity calibration

- **Reject / close recommendation** — invalid premise, duplicate/stale work, unreachable problem, or complexity whose carrying cost exceeds the value.
- **Must fix** — wrong operation can execute, security/data boundary weakens, public contract breaks, central claim is false, or required checks block safe integration.
- **Should fix / useful comment** — confirmed defect or material evidence gap with limited blast radius.
- **Risk / question** — worth reporting separately, but not represented as a confirmed defect.
- **No blocking findings** — reviewed obligations pass based on available evidence. This is not approval.

## Comment content

Lead with the side effect and affected contract. Include a fix suggestion only when the user asks or repository norms expect it. Follow the repository's normal language and tone; avoid decorative severity tags unless requested.
