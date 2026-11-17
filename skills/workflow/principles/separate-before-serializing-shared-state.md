# Separate Before Serializing Shared State

Before concurrent actors write one file, branch, key, or object, ask whether they need shared state or are publishing independent facts. Prefer separate owned outputs and combine them when reading. Separate fields in one `state.json` are still shared mutation.

When one shared target is a real invariant, serialize it structurally with a single writer, lock, sequential phases, or compare-and-swap. Instructions are not concurrency control.

Use the [worktree lifecycle](../workflows/pr/worktree/workflow.md) when branch isolation is needed; do not create duplicate checkouts for one branch. Keep each external checkpoint/log single-writer. Before takeover, reconcile the old writer and its live processes: an advisory message or cancellation request alone does not establish a stop. Preserve resources of unknown ownership.
