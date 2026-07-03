# Priority Labels

Use this reference after the review verdict is clear, before the final user report.

## Label set

Use exactly one existing priority label on every non-merged PR review:

| Label | Use when |
|---|---|
| `priority: p0` | Urgent blocker: security boundary break, data loss, startup/core outage, or severe regression with no practical workaround. |
| `priority: p1` | Important user-impacting issue, core runtime/provider/channel behavior change, API/compatibility risk, merge conflict, failing required CI, or a valid blocker that should be handled soon. |
| `priority: p2` | Default: clean review, low-risk bugfix, docs/tests/refactor, ordinary enhancement, minor edge case, or unvalidated proposal. |

## Required helper

Use the bundled helper, not `gh pr edit`, so label changes go through the REST issue-label API and avoid GraphQL project-card failures:

```bash
python3 <this-skill>/scripts/set_priority_label.py <PR> --repo <OWNER/REPO> --priority p1
```

The helper:

- removes/replaces only existing `priority: p*` labels
- preserves every non-priority label already on the PR
- never adds `valid`; it does not manage other non-priority labels
- verifies that exactly one priority label remains after the write

Dry-run first if unsure:

```bash
python3 <this-skill>/scripts/set_priority_label.py <PR> --repo <OWNER/REPO> --priority p1 --dry-run --format markdown
```

## Other labels

Never add `valid`. Other labels may be added when the review warrants it; no separate authorization is needed. They are separate from the priority helper, so use the appropriate label API for those changes and mention them in the final report.
