# Capture Guidance

Use this reference for model judgment while capturing an idea.

## What The Model Should Do

Use the model to understand and compress the source:

- Decide what the idea really is, not just where it came from.
- Choose a concise human title and filename.
- Match the user's language for the visible note.
- Separate human meaning from machine metadata.
- Extract enough evidence that a future agent can compare ideas without rereading the whole source.
- Decide whether existing ideas are genuinely related.

Use `scripts/idea_store.py` for mechanical actions:

- Resolve the store.
- Find by `id`, `source_id`, or file path.
- List existing notes.
- Write or update notes.
- Mark lifecycle status.
- Delete exactly matched notes.

## Relation Rules

Add `related` links only when there is a concrete relationship:

- Same source issue, incident, discussion, or user goal.
- Explicit duplicate, supersedes, follow-up, or blocked-by relationship.
- Same project plus same component, changed-file surface, or workflow boundary.
- One idea materially affects the selection or completion of another.

Do not link only because two ideas share a broad project, vague theme, similar priority, or similar cost.

## Cost

- `low`: a useful probe is one small step.
- `medium`: needs one focused work block.
- `high`: likely needs half a day or cross-module work.
- `unknown`: evidence is insufficient.

## Impact

- `low`: local cleanup or optional polish.
- `medium`: meaningful workflow, review, or maintainability improvement.
- `high`: user-visible capability, core reliability, data-loss/security risk, or unblocker for other work.
- `unknown`: evidence is insufficient.

## Confidence

- `high`: source evidence is concrete and current.
- `medium`: source evidence is plausible but incomplete or stale.
- `low`: idea is speculative, ambiguous, or missing key context.

## Source-Specific Evidence

For PRs and issues, capture useful facts such as status, checks, mergeability, conflicts, changed-file scope, linked issues, and main blocker. Keep tracker identifiers and URLs in metadata, not the body.

For conversation ideas, capture the user's motivation, the current design pressure, and the smallest next probe.

For file or URL ideas, capture the source path or URL in metadata and summarize only the relevant claim or opportunity in the body.
