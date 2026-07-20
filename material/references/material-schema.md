# Material Note Schema

Use this reference when creating or updating a material fragment.

## Store Config

The durable store config is:

```json
{ "materials_dir": "/absolute/path/to/material" }
```

The helper script resolves it from `$CODEX_HOME/material-store.json`, or `~/.codex/material-store.json` when `CODEX_HOME` is unset.

## Note Shape

Each material fragment is one Markdown file in the material directory.

Machine-facing metadata lives in YAML frontmatter:

```yaml
---
id: mat-YYYYMMDD-short-topic
created: YYYY-MM-DD
topic:
  - agent
  - prompt-caching
kind: finding
verification: verified
maturity: raw
platforms:
  - tweet
  - hn
source_url: ""
related:
  - "[[semantic-note-name]]"
events:
  - "YYYY-MM-DD captured"
---
```

The visible body is for humans:

```markdown
# Human-readable title

## Core Facts

Concrete, verifiable facts: numbers, code paths, measured results, tool names with versions.

## Evidence

How the facts were verified. What was measured, tested, or observed.

## Notes

Potential content angles, connections to other fragments, what's still missing.
```

## Metadata

Required metadata:

- `id`: stable internal id. Format `mat-YYYYMMDD-short-topic`.
- `created`: capture date.
- `topic`: list of topic tags. Used for grouping and filtering.
- `kind`: `finding`, `experiment`, `pitfall`, `tool-comparison`, `opinion`, or `resource`.
- `verification`: `verified`, `unverified`, or `hypothesis`.
- `maturity`: `raw`, `incubating`, `ready`, `published`, or `archived`.
- `platforms`: list of potential target platforms: `tweet`, `hn`, `longform`.
- `source_url`: source URL, or empty string.
- `related`: Obsidian wiki links to related material files, or empty list.
- `events`: append-only lifecycle events.

## Kind Values

- `finding`: a discovery from debugging, profiling, or investigation. The core asset type.
- `experiment`: a controlled comparison (A/B, before/after) with measured results.
- `pitfall`: a trap or unexpected behavior worth warning others about.
- `tool-comparison`: head-to-head evaluation of tools, configs, or approaches.
- `opinion`: a viewpoint backed by experience. Needs higher evidence bar than other kinds.
- `resource`: a verified link, tool, or reference worth endorsing.

## Maturity Lifecycle

- `raw`: just captured. May be a single sentence with one fact.
- `incubating`: has enough evidence to see a content angle, but needs more data or validation.
- `ready`: can be assembled into a draft frame. Has verifiable facts + a clear point.
- `published`: already used in published content. Keep for reference and follow-up.
- `archived`: decided not to pursue. Keep to avoid re-capturing the same thing.

## Verification Levels

- `verified`: you measured, tested, or directly observed this. You have logs, numbers, or code paths.
- `unverified`: plausible from reading docs or others' reports, but you have not tested it yourself.
- `hypothesis`: your inference or speculation. Needs evidence before promotion.

## Filenames

Use a short semantic filename that helps a human recognize the fragment in Obsidian. Do not use abstract ids, dates, or raw tracker ids unless the user explicitly asks.

Match the user's language. For a Chinese fragment, prefer a concise Chinese filename when it is readable on the user's filesystem. Preserve canonical code terms when translation would reduce clarity.

If a filename collides, add a semantic qualifier such as the topic or component.

## Script Payload

Use `scripts/material_store.py write` with JSON like:

```json
{
  "filename": "semantic-name.md",
  "title": "Human-readable title",
  "metadata": {
    "id": "mat-20260720-ollama-template-caching",
    "created": "2026-07-20",
    "topic": ["agent", "prompt-caching", "ollama"],
    "kind": "finding",
    "verification": "verified",
    "maturity": "raw",
    "platforms": ["tweet", "hn"],
    "source_url": "",
    "related": [],
    "events": ["2026-07-20 captured"]
  },
  "sections": {
    "Core Facts": "Concrete verifiable facts.",
    "Evidence": "How the facts were verified.",
    "Notes": "Content angles and connections."
  }
}
```

Use section headings in the user's language when the fragment is in Chinese.
