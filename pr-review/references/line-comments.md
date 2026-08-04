# PR line comments

Anchor a confirmed useful finding after the finding itself is established.

```bash
python <skill>/scripts/changed_line.py <PR> --repo <OWNER/REPO> --file <path> --line <line>
python <skill>/scripts/changed_line.py <PR> --repo <OWNER/REPO> --file <path> --pattern '<unique text>'
```

The helper verifies changed-line eligibility and emits `{path,line,side}`. Use `--side LEFT` for deleted code.

When a line is outside the diff, anchor to the changed line that creates the effect or keep the concern in the review body. Read only the narrow surrounding range needed to disambiguate the target.

State trigger, affected contract, consequence, and evidence in the repository's normal language. Use the legacy `position` fallback from `github-submission.md` when GitHub rejects a valid line/side anchor.
