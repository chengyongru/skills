# Make Operations Idempotent

Design operations so they converge to the correct state regardless of how many times they run or where the previous run stopped. Every state-mutating operation should answer: "What happens if this runs twice? What happens if the previous run crashed halfway?"

**Why:** Commands, lifecycle operations, and processing loops run where crashes, restarts, and retries are normal. If partial state changes the next run's outcome, every restart becomes a debugging session.

**The idea:** derive each step from the state that exists, not from what the previous run meant to do. Read the current state, compare it to the goal, and apply only the difference. A step written this way is safe to repeat, because a repeat finds nothing left to do.

Anything an owned run leaves behind, such as a lock, temporary file, partial record, or claimed job, should be reconcilable by the next run. Judge staleness by ownership and current process/artifact evidence, not timestamps alone. Unknown ownership means preserve and investigate, not delete. For example, atomically replace an owned checkpoint or compare artifacts by content instead of creation order. Keep run state outside the installed plugin under `.nanobot-workflows/runs/<run>/` with one writer.

**The test:**
1. What happens if this runs twice in a row?
2. What happens if the previous run crashed at every possible point?
3. Does re-execution converge to the same end state?

If any answer is "it depends on what state was left behind," the operation needs a reconciliation step.

Idempotence is not permission to retry a publication or destructive action. Inspect current local state before repeating a local mutation; for an authorized remote action, also re-read the relevant remote target/head and effect state. Commit, push, PR/review/merge, ticket, message, and deletion operations still need their actual authorization. Use supported idempotency keys or exact target/head checks when available; otherwise hold an uncertain effect instead of risking a duplicate. On restart, reconcile facts and start fresh bounded work, not a stale private child ID. Do not change a user-requested cadence or create a retry schedule automatically.
