# Subtract Before You Add

When evolving a system, remove complexity first, then build. Default to subtraction.

Make simplification a continual investment. Leave the design slightly simpler and more capable behind the same or smaller surface than you found it.

- Sequence proven in-scope removal before construction when it leaves a verifiable base.
- Cut unnecessary structure before polishing it; keep required behavior and compatibility.
- Design for observed usage and supported contracts, not speculative growth.
- Remove a validator/guard only after proving its invariant elsewhere for all reachable callers. External, tool, child, and history inputs still cross trust boundaries; unobserved attacks are not evidence that a safety check is dead.
- Simplify prompts by removing redundant instructions/templates while retaining authority, ownership, failure, and safety boundaries.
- Delete an empty reference only when removal is authorized and its incoming links/consumers are handled. Never treat user data, untracked files, protected memory, or live plugin files as disposable complexity.

Use installed [simplify](../workflows/code/simplify/workflow.md) for behavior-preserving cleanup. Subtraction is a design preference inside the user's scope, not blanket deletion permission or a reason to weaken meaningful verification.
