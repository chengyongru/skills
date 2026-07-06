# Idea Note Schema

Use this reference when interpreting idea notes.

Each idea is one Markdown file in the configured idea directory. Machine-facing metadata is in YAML frontmatter; the visible body is human-readable.

Important frontmatter keys:

- `id`: stable internal id.
- `status`: `open`, `doing`, `done`, `dropped`, or `duplicate`.
- `project`: project or life area.
- `kind`: source kind.
- `source_id`: stable source id, or `none`.
- `source_url`: source URL, or empty string.
- `title`: human-readable title.
- `cost`: `low`, `medium`, `high`, or `unknown`.
- `impact`: `low`, `medium`, `high`, or `unknown`.
- `confidence`: `low`, `medium`, or `high`.
- `related`: Obsidian wiki links to related idea files.
- `events`: lifecycle history.

Useful body sections:

- `Why` / `为什么`
- `Current State` / `当前状态`
- `Evidence` / `证据`
- `Blocker` / `阻塞`
- `Next` / `下一步`

Use `scripts/idea_store.py list --status open --status doing` to collect candidates. Use `scripts/idea_store.py read` to inspect likely candidates. Use `scripts/idea_store.py mark` only when the user asks to start or change status.
