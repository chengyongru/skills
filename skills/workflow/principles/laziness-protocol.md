# Laziness Protocol

- **Consolidate decisions.** Do not repeat the same choice in several places. Put it behind one source of truth and pass the result as a simple flag.
- **Minimize the justified diff.** Make the smallest change that meets the requested contract with meaningful proof. Fewer lines beat speculative boilerplate, not required validation, compatibility, accessibility, or tests.
- **Reuse the right tool.** Use installed [simplify](../workflows/code/simplify/workflow.md) for behavior-preserving cleanup and existing repository checks before inventing a helper. A read-only answer need not produce files.
- **Do not optimize away boundaries.** Keep unrelated work intact, do not hide a broader behavior change as cleanup, and do not weaken a gate to shrink the diff. Commit, publication, history edits, and deletion remain conditional on user scope.
