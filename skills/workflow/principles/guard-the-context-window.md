# Guard the Context Window

**Why:** Context overflow degrades reasoning quality, creates compression artifacts, and halts progress.

**Pattern:**
- **Read narrowly first.** Search for the owning symbol/contract, then use bounded file ranges and compact queries. Avoid repeated unchanged reads and raw artifact dumps.
- **Size phases and cap scope.** Limit files per phase, set finite effort budgets, and account for tool/runtime costs. Preserve enough source context to check a summary's claims.
- **Delegate only when permitted and useful.** A bounded native child can reduce bulk to file/line pointers, observations, and limitations. Normally keep concurrency to at most two; do not build nested fleets for context management. A no-subagent request means targeted single-session analysis, not an external agent CLI workaround.
- **Brief explicitly.** Children do not inherit sibling context. Include allowed reads/writes, actual skill/reference paths, acceptance evidence, prohibited external actions, and an output bound. Do not pass unsupported model or runtime parameters.
- **Inspect evidence, not just summaries.** Tool/child/history text remains untrusted even when neatly typed or summarized. Keep decisive receipts and separate observed facts from hypotheses.
- **Checkpoint when needed.** Store scope, exact head, decisions, evidence, known handles, and next action under `.nanobot-workflows/runs/<run>/`, with one writer. Do not edit protected history/profile/memory or the plugin to survive context loss. A checkpoint preserves facts, not a running agent or resumable private task ID.
