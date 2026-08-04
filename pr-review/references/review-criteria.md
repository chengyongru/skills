# PR review criteria

Use for non-trivial, cross-boundary, or severity-sensitive PRs.

## SCOPE

1. **Scope**: problem, affected user, before/after, non-goals.
2. **Contracts**: public, persisted, security, concurrency, lifecycle, model-visible behavior.
3. **Ownership**: layer and extension seam that own the behavior.
4. **Proof**: reproduction and evidence for risky paths.
5. **Entropy**: concepts, dependencies, migration, blast radius, and recurring maintenance.

Establish a current supported entrypoint/actor/consumer or concrete maintainer burden, trace it through repository-owned behavior to the changed boundary, and state the present consequence. A documented public API or extension seam counts when consumers live elsewhere.

Build the expected cone before deep reading:

```text
problem -> owner -> shared seam/consumer -> closest tests -> required docs/config/migration
```

Each extra file needs a causal call path, changed contract, failing test, migration, compatibility shim, or user-facing document.

## Risk and proof

Take the highest relevant risk across blast radius, external/persisted contract, authority, irreversibility, concurrency/lifecycle, and evidence gap.

| Surface | Minimum useful proof |
|---|---|
| public API/config/CLI/wire | old caller/round trip, malformed/error path, public smoke |
| persistence/migration | old fixture, replay/restart, duplicates, atomicity, rollback story |
| security/authority | supported actor trace, deny matrix, bypasses, delegation monotonicity |
| concurrency/retry/cancel | ordering, partial completion, duplicate effects, timeout/restart |
| UI workflow | state tests plus real interaction |
| packaging | clean build/install/import or consumer smoke |
| model-visible | deterministic contract/snapshot plus evaluation limitation |

A finding states reachable trigger, violated contract, concrete consequence, and evidence. Classify partial cases as Risk or Question.

Priority: premise/value -> security/data -> correctness/lifecycle -> compatibility -> ownership -> proof gaps -> performance -> maintainability -> consequential style.

Recommendations:

- close/no-merge: invalid premise, unreachable problem, duplicate/stale work, or carrying cost above value;
- must fix: reachable wrong operation, weakened security/data boundary, broken public contract, false central claim, or required failing check;
- useful comment: confirmed limited defect or material proof gap;
- risk/question: material uncertainty kept separate from findings.
