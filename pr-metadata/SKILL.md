---
name: pr-metadata
description: Inspect and update only a GitHub PR title and description. Use for explicit PR metadata requests or after a pushed PR fix makes the existing title/body inaccurate.
---

# PR Metadata

Keep the PR title and description aligned with the actual pushed scope. Do not change code, branches, labels, reviews, merge, closure, or other PR state.

1. Inspect the current metadata:

```powershell
python <skill>\scripts\pr_metadata.py inspect <PR> --repo <OWNER/REPO> --format json
```

2. Compare it with the actual PR diff and repository conventions. Preserve accurate context, issue links and closing keywords, template sections, checklists, and verification notes. Make no change when the metadata remains accurate.
3. Present the exact title/body change before mutation. An explicit metadata request authorizes it; when called by `pr-fix`, synchronizing stale metadata after the authorized pushed fix is part of fix completion.
4. Plan, then apply and verify the minimal replacement:

```powershell
python <skill>\scripts\pr_metadata.py update <PR> --repo <OWNER/REPO> --title $title --body $body --format markdown
python <skill>\scripts\pr_metadata.py update <PR> --repo <OWNER/REPO> --title $title --body $body --apply --format markdown
```

Omit `--title` or `--body` to preserve that field. Report before/after, changed fields, verification, and no-op state.
