# Migrate Callers Then Delete Legacy APIs

Use one coordinated, verifiable unit for a genuinely internal API migration: update the model and known callers, prove their contract, then remove the obsolete internal API. Avoid a permanent parallel abstraction when all consumers are under the same approved change boundary.

**Establish applicability first:**
- There is evidence that no supported external consumer needs the old API; absence of a local call is not enough for a public extension contract.
- The user authorized the relevant contract change and all callers are inside the task's coordinated scope.
- Any temporarily incomplete migration exists only in an isolated owned worktree, not a live/shared service or another agent's base.

**Execute:**
- Inventory static references plus configuration, strings, examples, documentation, and tests that act as callers.
- Migrate in dependency order and run meaningful caller/equivalence checks before removing the old entrypoint.
- Update tests for the intended contract. Delete an implementation-detail test only after its useful behavior coverage is preserved; do not remove a regression test merely because it fails during the migration.
- If external consumers, persistence, deployment ordering, or compatibility obligations exist, use an explicit compatibility/deprecation plan instead. Do not force a breaking change to satisfy this principle.

Report out-of-scope consumers and the smallest additional decision needed.
