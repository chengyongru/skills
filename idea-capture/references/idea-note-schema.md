# Idea Note Schema

Use this reference when creating or updating an idea note.

## Store Config

The durable store config is:

```json
{ "ideas_dir": "/absolute/path/to/idea" }
```

The helper script resolves it from `$CODEX_HOME/idea-store.json`, or `~/.codex/idea-store.json` when `CODEX_HOME` is unset.

## Note Shape

Each idea is one Markdown file in the idea directory.

Machine-facing metadata lives in YAML frontmatter:

```yaml
---
id: idea-YYYYMMDD-short-source
created: YYYY-MM-DD
status: open
project: project-or-area
kind: conversation
source_id: none
source_url: ""
title: "Human-readable title"
cost: low
impact: medium
confidence: high
related:
  - "[[semantic-note-name]]"
events:
  - "YYYY-MM-DD captured"
---
```

The visible body is for humans:

```markdown
# Human-readable title

## Why
Why this might matter.

## Current State
What is known now.

## Evidence
Concrete facts from the source.

## Blocker
What prevents immediate progress.

## Next
One concrete next action.
```

## Metadata

Required metadata:

- `id`: stable internal id. Keep it stable across filename changes.
- `created`: capture date.
- `status`: `open`, `doing`, `done`, `dropped`, or `duplicate`.
- `project`: project or life area.
- `kind`: `conversation`, `github-pr`, `github-issue`, `file`, `url`, or `note`.
- `source_id`: stable source id, or `none`.
- `source_url`: source URL, or empty string.
- `title`: human-readable title in the user's language.
- `cost`: `low`, `medium`, `high`, or `unknown`.
- `impact`: `low`, `medium`, `high`, or `unknown`.
- `confidence`: `low`, `medium`, or `high`.
- `related`: Obsidian wiki links to related idea files, or empty list.
- `events`: append-only lifecycle events.

Keep PR numbers, issue numbers, raw URLs, and source ids in metadata. Do not surface them in the visible body unless the user explicitly asks.

## Filenames

Use a short semantic filename that helps a human recognize the idea in Obsidian. Do not use abstract ids, dates, PR numbers, issue numbers, or raw tracker ids unless the user explicitly asks.

Match the user's language. For a Chinese idea, prefer a concise Chinese filename when it is readable on the user's filesystem. Preserve canonical code terms when translation would reduce clarity.

If a filename collides, add a semantic qualifier such as the project, component, or workflow area.

## Script Payload

Use `scripts/idea_store.py write` with JSON like:

```json
{
  "filename": "semantic-name.md",
  "title": "Human-readable title",
  "metadata": {
    "id": "idea-YYYYMMDD-short-source",
    "created": "YYYY-MM-DD",
    "status": "open",
    "project": "project-or-area",
    "kind": "conversation",
    "source_id": "none",
    "source_url": "",
    "title": "Human-readable title",
    "cost": "low",
    "impact": "medium",
    "confidence": "high",
    "related": [],
    "events": ["YYYY-MM-DD captured"]
  },
  "sections": {
    "Why": "Why this might matter.",
    "Current State": "What is known now.",
    "Evidence": "Concrete facts from the source.",
    "Blocker": "What prevents immediate progress.",
    "Next": "One concrete next action."
  }
}
```

Use section headings in the user's language.
