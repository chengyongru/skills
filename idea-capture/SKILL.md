---
name: idea-capture
description: Save, update, link, mark, or delete an idea, task candidate, PR, issue, project thought, conversation insight, or outcome in the user's Markdown idea directory. Use for capture requests and status changes such as done, dropped, duplicate, reopened, or doing.
---

# Idea Capture

Use model judgment for meaning, wording, relationships, cost, impact, and confidence. Use `scripts/idea_store.py` for every storage operation.

1. Resolve the store with `resolve`; use `--dir <dir> --create --save` for a user-specified location, or ask one setup question when no store exists.
2. For a new or substantial update, read `references/idea-note-schema.md` and `references/capture-guidance.md`.
3. Search with `find`; use `list` for status or project scans before creating a note.
4. Compose note JSON from the source context and persist it with `write --note-json`.
5. Use `mark` for status changes after identifying one exact note by id, source id, URL, or path.
6. Use `delete` after resolving exactly one note through an exact locator.

Match the user's language in visible content while preserving canonical identifiers. End with `<Action>: <title-or-id> -> <path>` using `Captured`, `Updated`, `Marked`, or `Deleted`.
