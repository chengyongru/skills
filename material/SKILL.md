---
name: material
description: Capture, incubate, and review verifiable content fragments from engineering work for future posts. Use when the user asks to save a material or experience fragment, review what is ready to write, or update a fragment's maturity.
---

# Material

Store *what may be worth sharing*; use `idea-capture` for *what to do*. The handoff is `material -> draft -> rewrite`.

Use `scripts/material_store.py` for storage:

1. Resolve the store; create and save a user-provided directory, or ask one setup question.
2. Read `references/material-schema.md` and `references/capture-guidance.md` for captures and substantial updates.
3. Use `find` for a known topic and `list` with maturity/topic/kind filters for reviews.
4. Compose note JSON and persist it with `write --note-json`.
5. Use `mark` for `raw -> incubating -> ready -> published` after identifying one exact note.
6. Use `delete` after resolving exactly one id, URL, or path.

Every fragment needs a checkable anchor: measurement, code path, reproducible observation, source link, or concrete first-hand example. Set verification and maturity from current evidence.

For “what can I write?”, group `ready` fragments into angles and identify the next evidence needed by promising `incubating` fragments. Hand the selected frame to `draft`.

Match the user's language and end storage actions with `<Action>: <title-or-id> -> <path>`.
