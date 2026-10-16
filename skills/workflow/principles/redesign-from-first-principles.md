# Redesign From First Principles

Think as if the new requirement had been a foundational assumption, then deliver the smallest authorized change that moves toward that coherent shape. First-principles thinking is a design method, not a grant to rewrite everything.

- Read affected contracts and consumers and understand why the current design exists.
- Ask: "if we were writing this from scratch with this requirement, what would we build?" Compare that target with the real compatibility, persistence, deployment, and user constraints.
- Update the references that belong to the scoped change: types, callers, docs, examples, and rationale. Report any necessary out-of-scope migration instead of silently taking it over.
- Deliver verifiable increments in owned local work. Do not break shared/live states or remove required compatibility as a shortcut.
- Use installed [simplify](../workflows/code/simplify/workflow.md) for behavior-preserving cleanup and a matching verifier for changed behavior. A read-only design request produces an explanation/proposal, not implementation or publication.

This preserves option value while respecting the current contract and the user's requested boundary.
