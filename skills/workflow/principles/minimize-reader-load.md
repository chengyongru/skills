# Minimize Reader Load

Reader load has two independent costs: layers to trace and hidden or mutable state to remember. Reduce both, not just line count.

- Collapse wrappers, adapters, and pass-through methods that add no meaningful boundary. A single caller alone does not make a trust, compatibility, or lifecycle boundary redundant.
- Shrink state scope: returns over mutations, locals over fields, fields over module state, and module state over globals. Derive instead of synchronizing copies.
- Name an invariant once at the owning boundary rather than in every consumer.

Can a new reader quickly answer where a value comes from and what can change it? Treat 30 seconds as a heuristic, not a measured acceptance gate. Use [simplify](../workflows/code/simplify/workflow.md) for authorized cleanup and verify retained behavior.
