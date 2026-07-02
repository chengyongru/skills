# Line Comment Reference

Use this file only after you have a concrete blocker or useful comment worth posting.

## Timing rule

Do not confirm inline line numbers during general exploration. First decide the finding. Then anchor it.

## Preferred source of line numbers

Use actual file line numbers from the isolated review/merge worktree, not diff-relative positions.

Good commands:

```bash
nl -ba <file> | sed -n '<start>,<end>p'
grep -n '<symbol-or-unique-text>' <file>
```

The line must be in the PR diff on the side you comment on. For new/modified code, use:

```json
{ "path": "<file>", "line": <actual-file-line>, "side": "RIGHT" }
```

For deleted code, use `side: "LEFT"` and the base-side line.

## Avoid repeated reads

- Do not reread the whole file once the finding is known.
- Read a narrow range around the target line and enough surrounding context to avoid anchoring to the wrong duplicate.
- If the same text appears multiple times, use a more specific grep or nearby function/class name.

## If GitHub rejects line + side

Then and only then use the legacy diff `position` fallback from `references/github-submission.md`.
