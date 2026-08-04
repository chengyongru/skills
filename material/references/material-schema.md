# Material note schema

Config resolution:

1. `$MATERIAL_CONFIG_HOME/material-store.json`
2. `$XDG_CONFIG_HOME/material/material-store.json`
3. `~/.config/material/material-store.json`

Config shape: `{ "materials_dir": "/absolute/path" }`.

Each fragment is one Markdown file with metadata:

| Field | Values / meaning |
|---|---|
| `id` | stable `mat-YYYYMMDD-short-topic` |
| `created` | `YYYY-MM-DD` |
| `topic` | list used for grouping |
| `kind` | `finding`, `experiment`, `pitfall`, `tool-comparison`, `opinion`, `resource` |
| `verification` | `verified`, `unverified`, `hypothesis` |
| `maturity` | `raw`, `incubating`, `ready`, `published`, `archived` |
| `platforms` | `tweet`, `hn`, `longform` |
| `source_url` | URL or empty string |
| `related` | Obsidian links or `[]` |
| `events` | append-only lifecycle events |

Visible sections: `Core Facts`, `Evidence`, `Notes`, translated to the user's language. Use a short semantic filename and a topic/component qualifier for collisions.

`material_store.py write --note-json` accepts inline JSON, a JSON path, or stdin:

```json
{
  "filename": "semantic-name.md",
  "title": "Human title",
  "metadata": {
    "id": "mat-YYYYMMDD-topic",
    "created": "YYYY-MM-DD",
    "topic": ["agent"],
    "kind": "finding",
    "verification": "verified",
    "maturity": "raw",
    "platforms": ["tweet"],
    "source_url": "",
    "related": [],
    "events": ["YYYY-MM-DD captured"]
  },
  "sections": {"Core Facts": "...", "Evidence": "...", "Notes": "..."}
}
```
