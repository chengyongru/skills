---
name: idea-capture
description: Save, update, link, or delete an idea, task candidate, PR, issue, project thought, conversation insight, or outcome in the user's Markdown idea directory. Use when the user invokes $idea-capture, says to remember/save/capture/log an idea, says an existing idea is done, dropped, duplicate, or reopened, or asks to delete/remove/clean a completed or unwanted idea.
---

# Idea Capture

## Idea Store

Resolve the idea directory in this order:

1. Use an explicit directory from the request.
2. If the request names an existing idea `.md` file, use that file as the target and its parent as the idea directory.
3. Read `$CODEX_HOME/idea-store.json`, or `~/.codex/idea-store.json` if `CODEX_HOME` is unset.
4. If no durable location is known, ask one setup question for the idea directory. If the current workspace looks like a notes repo (`.obsidian`, `content/idea`, `content/notebook`, or `notebook`), mention that as a suggested location but do not write there without user confirmation.

Config shape:

```json
{ "ideas_dir": "/absolute/path/to/idea" }
```

If the user gives a directory, create it if needed and persist the absolute directory path in the config.

## File Format

Use one Markdown file per idea. Name the file with a short human-readable slug that describes the idea, not the internal `id` or external tracker number.

Match the user's language for the filename, title, visible note body, and final response. Keep metadata keys in English for search. Preserve canonical code names, commands, API names, file paths, and source titles when translating them would reduce clarity.

Examples:

- `slash-command-streaming.md`
- `cron-stream-metadata.md`
- `next-action-skill.md`

Keep machine-facing metadata in YAML frontmatter. Keep the note body human-readable and free of source URLs, PR numbers, issue numbers, or other tracker noise unless the user explicitly asks to surface them.

```markdown
---
id: idea-YYYYMMDD-short-source
created: YYYY-MM-DD
status: open
project: project-or-area
kind: conversation | github-pr | github-issue | file | url | note
source_id: stable-source-id-or-none
source_url: URL-or-none
title: short recognizable title
cost: low | medium | high | unknown
impact: low | medium | high | unknown
confidence: low | medium | high
related:
  - "[[slash-command-streaming]]"
  - "[[cron-stream-metadata]]"
events:
  - YYYY-MM-DD captured
---

# Short recognizable title

## Why
One sentence describing why it might matter.

## Current State
Current state, scope, and relevant surface area in one or two sentences.

## Evidence
Concrete facts from the source, such as benchmark result, failing check, affected files, user quote, or observed behavior.

## Blocker
What prevents immediate progress, or none known.

## Next
One concrete next action.
```

Use `related: []` when there are no concrete related ideas. Keep frontmatter fields as searchable `key: value` lines where possible.

Stable ID rules:

- Use lowercase ASCII letters, digits, and hyphens.
- For GitHub PRs, use `id: idea-YYYYMMDD-github-pr-N` and `source_id: github-pr-N`.
- For GitHub issues, use `source_id: github-issue-N`.
- For URLs, use a short slug from the hostname or page title.
- Keep `id:` stable across filename changes. Use filenames for human readability and wiki links; use `id:` and `source_id:` for exact agent lookup.

Filename rules:

- Use lowercase ASCII letters, digits, and hyphens.
- Keep names short, meaningful, and readable in Obsidian's file list.
- Prefer semantic names such as `document-attachments.md`, `edit-file-target-lines.md`, or `next-action-skill.md`.
- Do not put PR numbers, issue numbers, dates, or abstract ids in filenames unless the user explicitly asks.
- If a filename would collide, add a semantic qualifier such as the project, component, or workflow area.
- Do not name files only from the abstract `id` or source tracker id.
- For Chinese requests, avoid long English prose in filenames or the visible note body. Use Chinese for human-readable text and keep only necessary technical terms in English.

Useful exact line patterns include `^source_id: github-pr-4635$`, `^status: open$`, `^impact: high$`, and `^project: nanobot$`.

## Capture Workflow

Read or search the idea directory before writing. If a matching `id` or `source_id` already exists, update that file instead of creating a duplicate. Append one new file by default for a new idea. Do not ask for a form. Infer from the current context and keep unknowns short.

Status is lightweight filtering metadata, not a task board:

- `open`: not chosen yet
- `doing`: currently being advanced
- `done`: completed or merged
- `dropped`: intentionally abandoned
- `duplicate`: superseded by another entry

Cost scale:

- `low`: a useful probe fits in one small step
- `medium`: needs one focused work block
- `high`: likely needs half a day or cross-module work

Impact scale:

- `low`: local cleanup or optional polish
- `medium`: meaningful workflow, review, or maintainability improvement
- `high`: user-visible capability, core reliability, data-loss/security risk, or unblocker for other work

Rules:

- Always include a concrete `## Next` section.
- Always include enough `## Current State` and `## Evidence` for a future agent to compare this idea without rereading the whole source.
- For PRs/issues, capture status, checks, mergeability/conflicts, changed-file scope, linked issues, and the main blocker when available.
- Put source IDs, source URLs, tracker numbers, and raw links only in frontmatter metadata, not in the visible note body.
- For `related:`, search existing idea files and add wiki links only in frontmatter when there is a concrete relationship: same source issue, explicit mention, duplicate/supersedes/follow-up, blocking relationship, or the same project plus the same component or changed-file surface.
- Do not link ideas merely because they share a broad project, vague theme, or similar priority.
- Add related links to the created or edited file using the target idea's filename without `.md`. Do not rewrite backlinks in older files unless the user asks.
- If the user says an existing idea is done, dropped, duplicate, reopened, or currently being worked on, update the matching file's `status:` line and append one entry under `events:`.
- If the user asks to delete/remove/clean an idea, locate exactly one file by `id` or `source_id` and delete that idea file.
- Never delete by fuzzy title alone. If there is no stable id/source id or more than one possible match, ask one short disambiguation question.
- For "done" without an explicit delete/remove/clean request, mark `status: done`; do not delete.
- If multiple entries match a status/outcome update, ask one short disambiguation question.
- If invoked after another skill such as PR triage/review, treat that result as the source evidence.
- End with one line: `<Action>: <title-or-id> -> <path>`, where action is `Captured`, `Updated`, `Marked`, or `Deleted`.
