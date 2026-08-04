# Idea note fields

Each Markdown note has YAML metadata and a human-readable body.

- identity/context: `id`, `project`, `kind`, `source_id`, `source_url`, `title`;
- state: `status` (`open`, `doing`, `done`, `dropped`, `duplicate`) and `events`;
- judgment hints: `cost`, `impact`, `confidence`, `related`;
- body: `Why`, `Current State`, `Evidence`, `Blocker`, `Next` in the note's language.

Use `list --status open --status doing`, then `read` likely candidates. Use `mark` when the user starts or changes one note's status.
