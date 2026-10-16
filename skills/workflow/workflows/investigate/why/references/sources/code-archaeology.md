# Code Archaeology (git + in-repo)

## What this source contains

- Commit history (messages, dates, authors, diffs)
- PR descriptions, review comments, and discussion threads (via `gh`)
- Inline code comments, TODOs, FIXMEs, deprecation notes
- ADRs (architectural decision records) if the repo keeps them
- Tests, whose names and assertions often encode the edge cases that motivated a change
- Related files modified in the same commits (co-change signal)
- CHANGELOG entries and release notes in the repo
- Issue/ticket IDs in commit messages and PR bodies

This source ties evidence directly to the code, but shallow clones, rewritten history, missing PR access, and incomplete comments can leave gaps. Check those limits rather than assuming the repository contains every decision.

## How to search it

Confirm the actual repository and available Git/`gh` reads first. Use `exec` with that working directory. The examples below are command templates: substitute and quote actual paths/revisions before execution in PowerShell; angle-bracket placeholders are not literal shell syntax. Read only; do not fetch, checkout, reset, commit, or publish implicitly.

Expand the seed commit list:

```powershell
# History through renames
git log --follow --oneline -- <file>

# Pickaxe: commits that added or removed this exact text
git log -S '<exact_string_from_code>' -- <file>

# Or for patterns:
git log -G '<regex>' -- <file>

# Who wrote each line and when
git blame -L <start>,<end> <file>

# One commit's full diff
git show <hash>

# Commits between two points affecting this file
git log <old>..<new> -p -- <file>
```

Look for out-of-band docs with native `rg`/file reads:

```powershell
# ADRs often live in docs/adr/ or similar
rg -l -i 'architecture.decision' --glob '*.md'

# TODOs and FIXMEs near the target
rg -n -C2 '(TODO|FIXME|HACK|XXX|NOTE)' <target_file>

# Related tests
rg -l '<symbol>' --glob '*test*'
```
