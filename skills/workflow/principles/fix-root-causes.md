# Fix Root Causes

Fix the first wrong decision or unhandled legitimate state, not the place where its symptom surfaced.

- Reproduce first and trace a regression to its introducing change. Ask why until the answer is a fault rather than an earlier fault's consequence. Use actual state and errors; instrument only an authorized owned reproduction.
- Decide whether the triggering state is legitimate. Handle it where the code broke if it is; otherwise find what produced it. Guards, retries, swallowed errors, clamping, and discarded state can hide the original bug.
- Find the same fault in reachable in-scope callers. A causal repair outside the task is a dependency to report, not an automatic scope expansion. For restart-only failures, inspect persisted state.
- If the decisive fact required a deep investigation, propose the cheap ongoing signal that would expose it earlier.

Keep useful warnings until the underlying condition is understood. A long workaround comment is a reason to inspect the design, not proof that deleting the comment or code is safe.
