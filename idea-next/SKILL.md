---
name: idea-next
description: Choose one concrete next action from the user's Markdown idea directory. Use when the user invokes $idea-next or asks what to do next, what to work on now, which idea, PR, or project to advance, or how to break choice paralysis using captured ideas.
---

# Idea Next

Use model judgment to choose the action that best changes the user's situation now. Use `scripts/idea_store.py` for storage mechanics.

1. Resolve the store with `resolve`; ask one setup question when no store exists.
2. Read `references/idea-note-schema.md` and `references/selection-guidance.md`.
3. List open/doing candidates, filter to the requested scope, and read the strongest candidates.
4. Make at most three small source lookups when decisive context is missing.
5. Choose one action from evidence and tradeoffs. Provide a ranking only when requested.
6. Mark one note `doing` when the user asks to start it.

Match the user's language. Return the chosen action, why it wins now, and the first concrete step.
