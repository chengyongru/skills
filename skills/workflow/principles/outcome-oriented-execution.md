# Outcome-Oriented Execution

Optimize for the intended, verifiable end state without inventing compatibility scaffolding that has no consumer. Keep required compatibility and safe integration boundaries intact.

**Why:** Temporary adapters can become permanent debt. An isolated migration may need a brief incomplete local state, but shared systems and other workers cannot be treated as scratch space.

**Core rule:**
- Name the target contract and verification boundaries before moving structure.
- Allow a temporarily incomplete step only in an owned isolated worktree when planned, scoped, reversible, and not consumed by others.
- Do not break live/shared state, published APIs, required CI, persistence, or another worker's base to reach the target faster.

**Guardrails:**
- Preserve unrelated edits and coordinate one writer per branch or shared invariant.
- State exactly which local checks may be temporarily red, why, and the boundary that must restore them. Do not disable/soft-fail checks or relax acceptance criteria to hide breakage.
- Run high-signal checks as each coherent unit completes. Before integration/delivery, run the static and behavioral proof relevant to the reachable change; docs-only work does not need invented runtime or performance proof.
- If deployment order or external consumers require a compatibility period, plan it explicitly rather than deleting it on principle.
- Commit, rebase, publish, and merge only within authorization. A target architecture does not grant a wider rewrite or permission to leave shared work broken.
