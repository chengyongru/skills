# Idea note schema

Config: `{ "ideas_dir": "/absolute/path" }` in `$CODEX_HOME/idea-store.json`, falling back to `~/.codex/idea-store.json`.

Each idea is one Markdown file with YAML frontmatter:

| Field | Values / meaning |
|---|---|
| `id` | stable `idea-YYYYMMDD-short-source` |
| `created` | `YYYY-MM-DD` |
| `status` | `open`, `doing`, `done`, `dropped`, `duplicate` |
| `project` | project or life area |
| `kind` | `conversation`, `github-pr`, `github-issue`, `file`, `url`, `note` |
| `source_id` | stable source id or `none` |
| `source_url` | URL or empty string |
| `title` | human-readable title |
| `cost`, `impact` | `low`, `medium`, `high`, `unknown` |
| `confidence` | `low`, `medium`, `high` |
| `related` | Obsidian links or `[]` |
| `events` | append-only lifecycle events |

Visible sections: `Why`, `Current State`, `Evidence`, `Blocker`, `Next`, translated to the user's language.

Use a short semantic filename in the user's language. Add a project/component qualifier for collisions. Keep tracker ids and raw URLs in metadata.

`idea_store.py write --note-json` accepts inline JSON, a JSON path, or stdin:

```json
{
  "filename": "semantic-name.md",
  "title": "Human title",
  "metadata": {
    "id": "idea-YYYYMMDD-source",
    "created": "YYYY-MM-DD",
    "status": "open",
    "project": "area",
    "kind": "conversation",
    "source_id": "none",
    "source_url": "",
    "title": "Human title",
    "cost": "unknown",
    "impact": "unknown",
    "confidence": "medium",
    "related": [],
    "events": ["YYYY-MM-DD captured"]
  },
  "sections": {"Why": "...", "Current State": "...", "Evidence": "...", "Blocker": "...", "Next": "..."}
}
```
