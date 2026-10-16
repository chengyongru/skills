# Sequence work into verifiable units

Order work as a sequence of small units, each ending in a state you can check, and don't advance until the current one is green.

**Why:** A break caught at the unit that caused it is cheap to localize. A break caught after a batch is buried, and you have already built further on a broken base. Sequencing those same units into a delivery a reviewer can replay turns "trust me" into "watch it go red, then green."

**Execution.** In a sweep or migration, choose coherent units with a meaningful before/after check: known baseline, one scoped change, actual proof, then advance. Pin the current base/head and existing dirty state; do not rebase, reset, or discard work just to manufacture a clean baseline. Use installed [pr-worktree](../workflows/pr/worktree/workflow.md) for isolation where needed. Rebase only when authorized and actually needed for integration. Reuse a lever when it makes the per-unit check cheaper, without making a new script mandatory.

**Delivery.** If commits or PRs are authorized, order coherent slices so their evidence is understandable: a local failing test before the fix, a subtraction before a reshape, or a baseline before treatment. Demonstrate red-then-green without requiring a published broken commit. An independently delivered unit must meet its own contract; coupled internal migration steps stay isolated until their agreed boundary is green. Opening, pushing, or landing each unit is conditional, not ceremony.

A new head/base or dependency change requires fresh affected proof; unchanged patch text is not enough. Scale checks to the reachable behavior and report a blocked boundary rather than checking a box on inference.

The sequencing complement to the **prove-it-works** principle skill, which keeps each check real, and the **build-the-lever** principle skill, which makes the per-unit check cheap.
