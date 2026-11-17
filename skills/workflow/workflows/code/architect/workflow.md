# Architect

Before writing code, trace every system the change touches. If ownership or layering changes, use [why](../../investigate/why/workflow.md) to recover the constraints behind the existing shape. Sketch two structurally different designs, including caller usage, types, signatures, and module boundaries. Choose the one where each piece of state has one owner, each task has one way to do it, and callers need to know least.

For a large or contested design, use [arena](../../coordinate/arena/workflow.md) instead of sketching alone. The [runtime contract](../../../references/runtime.md) still controls delegation; if workers are unavailable or prohibited, compare the designs directly and state any unmet independent-review requirement. Ordinary design work does not require parallel candidates or a separate synthesizer.

Redesign rather than patch when workarounds repeat. If implementation exposes a wrong assumption, revisit the shape rather than bolt on special cases. Deliver the chosen sketch and its concrete tradeoff. A design-only request or user checkpoint stops before implementation; otherwise fill in the sketch within the authorized scope. Keep any requested design files outside the installed plugin.

For a consequential state machine or concurrency design, consider an explicitly bounded [Statechart](../../verify/statechart/workflow.md) check of the disputed invariant or interleaving. Keep it tied to the code's atomic boundaries; model checking is not required for settled mechanical work.
