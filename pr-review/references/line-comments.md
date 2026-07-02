# Line Comment Reference

Use this file only after you have a concrete blocker or useful comment worth posting.

## Timing rule

Do not confirm inline line numbers during general exploration. First decide the finding. Then anchor it.

## Preferred source of line numbers

Use the bundled anchor helper from the isolated review/merge worktree:

```bash
python3 <this-skill>/scripts/changed_line.py <N> --repo <OWNER/REPO> --file <path> --line <actual-file-line>
python3 <this-skill>/scripts/changed_line.py <N> --repo <OWNER/REPO> --file <path> --pattern '<unique text>'
```

It checks whether the line is anchorable in the PR diff and emits the JSON skeleton:

```json
{ "path": "<file>", "line": <actual-file-line>, "side": "RIGHT" }
```

For deleted code, pass `--side LEFT`; the helper reads base-side deleted lines from the diff.

If the helper says the line is not in changed lines, do not force an inline comment there. Move the comment to the changed line that creates the side effect, or keep the concern in the review body only if body-only feedback is acceptable.

## Avoid repeated reads

- Do not reread the whole file once the finding is known.
- Read a narrow range around the target line and enough surrounding context to avoid anchoring to the wrong duplicate.
- If the same text appears multiple times, use a more specific grep or nearby function/class name.

## If GitHub rejects line + side

Then and only then use the legacy diff `position` fallback from `references/github-submission.md`.
