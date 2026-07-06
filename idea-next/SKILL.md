---
name: idea-next
description: Choose one concrete next action from the user's Markdown idea directory. Use when the user invokes $idea-next or asks what to do next, what to work on now, which idea/PR/project to advance, or how to break choice paralysis using previously captured ideas.
---

# Idea Next

Use the model for judgment: interpret evidence, compare tradeoffs, notice real dependencies, adapt to the user's language, and explain the selected action concretely.

Use `scripts/idea_store.py` for mechanics: resolve the store, list candidate notes, read likely candidates, and mark a note as `doing` only when the user asks to start.

## Workflow

1. Resolve the store with `python scripts/idea_store.py resolve`. If no store exists, ask one short setup question for the idea directory.
2. Read `references/idea-note-schema.md` and `references/selection-guidance.md`.
3. List candidates with `python scripts/idea_store.py list --status open --status doing`. Filter by project or user-specified scope when relevant.
4. Read the likely candidate notes with `python scripts/idea_store.py read`. If top candidates lack enough context, do at most three small source lookups total, then decide.
5. Choose one action. Do not produce a ranking unless asked.
6. If the user asks to start the chosen action, mark exactly one note with `python scripts/idea_store.py mark --status doing`.

## Language

Match the user's language in the recommendation. Avoid long English prose for Chinese requests except for code names, commands, file paths, API names, and canonical source titles.

## Output

Return exactly:

```markdown
做：<one action>

理由：<two or three concrete sentences grounded in the selected note's evidence/current state/blocker>

下一步：<first concrete probe, with no duration estimate>
```
