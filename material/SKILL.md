---
name: material
description: Capture, incubate, and review verifiable content fragments from daily engineering work — debugging findings, experiments, tool comparisons, pitfalls — for future social posts. Use when the user says to save/log/capture a material or experience fragment, asks what content is ready to write, or wants to review accumulated material fragments by topic or maturity.
---

# Material

Capture verifiable experience fragments from daily work and let them incubate until ready to draft.

The boundary with idea-capture: idea-capture stores *what to do* (action items, cost/impact/status). material stores *what to share* (verified facts, data points, conclusions with evidence). They run in parallel.

## Pipeline Position

```
material (capture → incubate → review/assemble) → draft (成稿) → rewrite (去AI味, optional)
```

material does not produce final copy. Its output is a draft frame: selected fragments + suggested angle + platform hint. Hand off to `draft` for final copy.

## Workflow

1. Resolve the store with `python scripts/material_store.py resolve`. If the user gives a directory, run `python scripts/material_store.py resolve --dir <dir> --create --save`. If no store exists, ask one short setup question for the material directory.
2. For a new capture or substantial update, read `references/material-schema.md` and `references/capture-guidance.md`.
3. Use `python scripts/material_store.py find "<query>"` to retrieve fragments by keyword. Use `python scripts/material_store.py list` with `--maturity`/`--topic`/`--kind` filters for review scans.
4. Compose the note JSON yourself from the source context, then write it with `python scripts/material_store.py write`.
5. For maturity updates (raw → incubating → ready → published), use `find` or `read` to identify the target, then `python scripts/material_store.py mark` with one exact locator: `--id`, `--source-url`, or `--path`.
6. For delete requests, use `python scripts/material_store.py delete` only after locating exactly one note by `id`, `source_url`, or file path.

## Core Capture Rules

- Every fragment must have at least one **checkable anchor**: a measurement, code path, reproducible observation, named resource with a source link, or concrete first-hand example. Unsupported opinions are not ready material.
- Set `verification` honestly: `verified` (measured, tested, directly observed, or checked against the source), `unverified` (plausible but not yet checked), `hypothesis` (speculation needing evidence).
- Judge `maturity` from current evidence. Default fragmentary captures to `raw`, but existing well-supported experiences may start as `incubating`, `ready`, or `published`.

## Review Mode

When the user asks "what can I write" or "review my materials":

1. `list --maturity ready` — these are immediately draftable.
2. `list --maturity incubating` — these need one more evidence push before they're ready.
3. Group ready fragments by `topic` and suggest content angles. Do not draft here — suggest and hand off to `draft`.

## Language

Match the user's language for filenames, titles, visible note bodies, and final responses. Keep metadata keys stable. Preserve canonical code names, commands, API names, file paths, and source titles when translating them would reduce clarity.

## Final Response

End with one line:

```text
<Action>: <title-or-id> -> <path>
```

Use `Captured`, `Updated`, `Marked`, or `Deleted` for the action.
