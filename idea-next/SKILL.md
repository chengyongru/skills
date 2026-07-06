---
name: idea-next
description: Choose one concrete next action from the user's Markdown idea directory. Use when the user invokes $idea-next or asks what to do next, what to work on now, which idea/PR/project to advance, or how to break choice paralysis using previously captured ideas.
---

# Idea Next

Use the model for judgment: choose the action that best changes the user's situation now, interpret evidence, compare tradeoffs, notice real dependencies, adapt to the user's language, and explain the selected action concretely.

Use `scripts/idea_store.py` for mechanics: resolve the store, list candidate notes, read likely candidates, and mark a note as `doing` only when the user asks to start.

## Workflow

1. Resolve the store with `python scripts/idea_store.py resolve`. If no store exists, ask one short setup question for the idea directory.
2. Read `references/idea-note-schema.md` and `references/selection-guidance.md`.
3. List candidates with `python scripts/idea_store.py list --status open --status doing`. Filter by project or user-specified scope when relevant.
4. Read the likely candidate notes with `python scripts/idea_store.py read`. If top candidates lack enough context, do at most three small source lookups total, then decide.
5. Choose one action using the decision core in `selection-guidance.md`. Do not score mechanically and do not produce a ranking unless asked.
6. If the user asks to start the chosen action, mark exactly one note with `python scripts/idea_store.py mark --status doing`.

## Language

Match the user's language and tone in the recommendation. Preserve code names, commands, file paths, API names, and canonical source titles when translating them would reduce clarity.

## Response

Answer naturally. Include the chosen action, the concrete evidence-based reason, and the first next step, but do not force fixed headings, labels, order, or formatting. Keep it concise unless the user asks for comparison or detail.
