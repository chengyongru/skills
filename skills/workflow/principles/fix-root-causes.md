# Fix Root Causes

When debugging, fix the fault, not the place where it surfaced. The symptom is where a wrong state became visible. The root cause is the first place the system did something it should not do, or failed to handle a state it should handle.

**Why:** A symptom fix hides the evidence and leaves the fault free to surface somewhere else. Each one makes the system harder to reason about, because the code now carries a workaround for a bug that nobody named.

**Pattern:**
- Reproduce first.
- Ask "why" at each step until the answer is a wrong decision in the code, not a consequence of an earlier one.
- When stuck, read the actual error and state. Use existing diagnostics first. Instrument only in an authorized owned reproduction, or obtain specific permission for disruptive/live probes. A read-only investigation is not permission to hot-patch the process.
- Ask whether the state that triggered the symptom is legitimate. If the system may be in that state, the code that broke on it is the root cause, and handling the state there is the fix. If the state should never exist, a check where it broke hides the bug. Find what produced the state. Guards, retries, swallowed errors, clamped values, and discarded state are the usual ways to hide a bug.
- When something fails only after a restart, suspect persisted state first: config files, caches, lock files, serialized state.
- Check for the pattern, not just the instance. Trace affected in-scope callers and correct reachable copies that belong to the authorized task. If the causal repair crosses that boundary, explain the dependency and obtain scope rather than fixing unrelated systems automatically.
- A long workaround comment is a reason to inspect the design, not proof that the code is wrong. Preserve compatibility and non-obvious constraints until evidence supports their removal.
- If the deciding fact took a deep dig to find, propose the cheap signal that would have exposed it earlier. Do not automatically change shared observability, live plugins, protected memory, tickets, or external messages.

The root-cause doctrine chooses where a justified fix belongs. It does not expand authorization, permit breaking shared/live state, or turn a diagnosis request into implementation. If the cause cannot be safely confirmed, report the strongest supported hypothesis and the missing check.
