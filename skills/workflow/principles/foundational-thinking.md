# Foundational Thinking

**Structural decisions** protect option value. **Code-level decisions** protect simplicity.

**Data structures first.** Get the data shape right before writing logic. Define core types early, trace every access pattern, and choose structures that match the dominant paths.

At code level, DRY the structure, not every line. Types and data models should converge. Three similar statements still beat a premature abstraction. Prefer explicit over clever. Test behavior and edge cases, not line counts.

**Concurrency corollary.** Before sharing state between actors, ask "what happens if another actor modifies this concurrently?" If not "nothing", isolate.

**Scaffold first when it is a real prerequisite.** Ask "does every subsequent phase benefit from this existing?" Shared types, fixtures, or a focused test may be the right first unit. Do not expand a small task into unrelated CI, lint, or framework work. Sequence for option value: necessary setup before features, a meaningful failing check before its fix. Make commits small and single-purpose only when commits are authorized.

Each increment should land a coherent abstraction or deepen one that exists. Do not spread a new capability across callers as special-case coordination.

Subtraction comes before scaffolding when the code is proven dead and removal is in scope. Preserve contracts, user data, and shared/live state. A better target model guides scoped incremental work; it does not justify a repository-wide rewrite or automatic publication.
