# Separate Before Serializing Shared State

When concurrent actors might share mutable state, first ask whether they need the same mutable object. If not, eliminate the sharing. When sharing is real, enforce serialization structurally: lockfiles, sequential phases, exclusive ownership. Instructions and conventions are not concurrency control.

**Why:** Concurrent writes to shared state create race conditions that are intermittent, hard to reproduce, and expensive to debug.

**Pattern:**
1. **Identify shared mutable state** (files both read and write, branches both push to, APIs both define and consume).
2. **Default: eliminate the shared write target.** Ask: do these actors need one canonical object, or are they publishing independent facts? Give each actor its own owned file, key, branch, or state directory, and merge only at the read/reporting boundary. Two workers writing their own `lastX` field into one `state.json` is still shared mutation. `indexer-state.json` + `metrics-state.json` is not.
3. **Only when one shared write target is a real invariant, serialize access structurally** (lockfiles, sequential phases, single-writer actor, or atomic compare-and-swap). Treat "we need a lock" as a design smell to check, not as the default answer.
4. **Respect existing ownership.** Use installed [pr-worktree](../workflows/pr/worktree/workflow.md): one branch maps to one registered worktree. Separate competing writers by distinct branches/worktrees or truly disjoint paths, not duplicate worktrees for the same branch. A topology owner must stop/reconcile a code writer before mutating its branch.
5. **Keep run records single-writer.** Put task state outside the plugin under `.nanobot-workflows/runs/<run>/`. Children report into their own files; one coordinator updates a shared checkpoint/log after inspecting the evidence. A file path in a prompt is not a lock.
6. **Reconcile before takeover.** Advisory `send` delivery is not a stop. If a child must be replaced, use `cancel` when necessary and confirm final task/process state before another writer starts. Preserve unknown locks/resources; do not kill unrelated processes or delete user state to clear a presumed stale owner.

Use a bounded native fan-out only when permitted, and honor a no-subagent request.
