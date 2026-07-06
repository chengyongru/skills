---
name: idea-capture
description: Save, update, link, or delete an idea, task candidate, PR, issue, project thought, conversation insight, or outcome in the user's Markdown idea directory. Use when the user invokes $idea-capture, says to remember/save/capture/log an idea, says an existing idea is done, dropped, duplicate, or reopened, or asks to delete/remove/clean a completed or unwanted idea.
---

# Idea Capture

Use the model for meaning: identify the actual idea, choose human-readable wording, adapt to the user's language, summarize evidence, judge cost/impact/confidence, and decide genuine related ideas.

Use `scripts/idea_store.py` for mechanics: resolve the store, list/read/find notes, write notes, mark status, and delete exactly matched files. Do not hand-edit idea files unless the helper cannot perform the operation.

## Workflow

1. Resolve the store with `python scripts/idea_store.py resolve`. If the user gives a directory, run `python scripts/idea_store.py resolve --dir <dir> --create --save`. If no store exists, ask one short setup question for the idea directory.
2. For a new capture or substantial update, read `references/idea-note-schema.md` and `references/capture-guidance.md`.
3. Use `python scripts/idea_store.py find` when an `id`, `source_id`, or file path is known. Use `python scripts/idea_store.py list` before creating a new note so duplicates and concrete related ideas can be detected.
4. Compose the note JSON yourself from the source context. Then write it with `python scripts/idea_store.py write`.
5. For done/dropped/duplicate/reopened/doing, use `python scripts/idea_store.py mark` after locating exactly one note.
6. For delete/remove/clean requests, use `python scripts/idea_store.py delete` only after locating exactly one note by `id`, `source_id`, or file path. Never delete by fuzzy title alone.

## Language

Match the user's language for filenames, titles, visible note bodies, and final responses. Keep metadata keys stable. Preserve canonical code names, commands, API names, file paths, and source titles when translating them would reduce clarity.

## Final Response

End with one line:

```text
<Action>: <title-or-id> -> <path>
```

Use `Captured`, `Updated`, `Marked`, or `Deleted` for the action.
