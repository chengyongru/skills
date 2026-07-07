# GitHub Review Submission Reference

Load this only after you have at least one blocker or useful comment and have anchored line numbers with `references/line-comments.md`.

## Rules

- Submit `COMMENT` reviews only.
- Never submit `APPROVE`.
- Do not submit `REQUEST_CHANGES` unless the user explicitly asks for that exact event.
- Do not create a GitHub review when there are no blockers/useful comments.
- Public GitHub review bodies and inline comments must be in English, regardless of the user's chat language. Use the user's language only for the local final report back to the user.
- Start the review body with the short English disclosure line `> Automated review from nanobot`.
- Include inline comments on specific changed lines. Do not post only a body summary when commenting on code.

## Build and submit payload

Write the payload builder to a temp file first. Do not use `python -c`; Markdown/backticks/quotes in review bodies are easy to break in shell strings.

```python
# /tmp/build_review.py
import json

body = (
    "> Automated review from nanobot"
    "\n\n"
    "Review body here. Keep it concise."
)

comments = [
    {
        "path": "<file path>",
        "line": <actual file line number>,
        "side": "RIGHT",
        "body": "Inline comment here",
    },
]

payload = {
    "body": body,
    "comments": comments,
    "event": "COMMENT",
}

with open("/tmp/review_payload.json", "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

print(f"Payload written: {len(comments)} inline comments")
```

```bash
python3 /tmp/build_review.py

gh api repos/<OWNER>/<REPO>/pulls/<N>/reviews \
  --input /tmp/review_payload.json \
  --jq '{id, state, html_url}'
```

Save the returned URL for the final local report.

## Fallback: diff position

Prefer `line` + `side`. If GitHub rejects the anchor even though the line is in the changed file, fall back to legacy `position`.

```bash
gh pr diff <N> --repo <OWNER>/<REPO> > /tmp/pr<N>.diff
```

`position` is the 1-based index of changed lines within that file's diff section, counting changed/context diff lines as GitHub expects and excluding file headers. Use this only as a fallback; actual file line + side is simpler.

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Asking for extra publish confirmation | COMMENT posting is already authorized by this skill when findings warrant it |
| Using `APPROVE` | Never approve from this skill |
| Posting a clean-review comment | Do not post when there are no blockers/useful comments |
| Missing disclosure | Start the body with `> Automated review from nanobot` |
| Posting body-only code feedback | Include inline comments anchored to changed lines |
| Using `python -c` for payload | Write a temp script/file first |
