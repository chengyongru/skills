# GitHub Review Submission Reference

Mechanical steps for creating, managing, and publishing GitHub PR reviews via the API.

**Core rule: ALWAYS create as PENDING. NEVER auto-publish.** The user must explicitly say "发布" before the review goes live.

The review MUST include inline comments on specific code lines (like a human would on the "Files changed" tab), not just a body summary.

## 1. Build JSON Payload and Create Pending Review

**CRITICAL: Do NOT include `event` field. Omitting `event` creates a PENDING review.** Setting `event: "PENDING"` causes a 422 error — PENDING is not a valid event value.

**Always write the payload script to a temp file first**, then execute it. **Never use `python -c "..."`** — review bodies contain backticks, markdown, and special characters that will break bash string parsing.

Inline comments use `line` (file line number) + `side` (`"RIGHT"` for new code, `"LEFT"` for deleted code). This is simpler and more reliable than the legacy `position` approach.

```python
# /tmp/build_review.py
import json

body = (
    "Review body here. "
    "Use string concatenation for multi-line content."
)

comments = [
    {
        "path": "<file path>",
        "line": <file line number>,
        "side": "RIGHT",
        "body": "Inline comment here",
    },
]

# No "event" field — omitting it creates a PENDING review
payload = {
    "body": body,
    "comments": comments,
}

with open("/tmp/review_payload.json", "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

print(f"Payload written: {len(comments)} inline comments")
```

```bash
python /tmp/build_review.py

gh api repos/<OWNER/REPO>/pulls/<N>/reviews \
  --input /tmp/review_payload.json \
  --jq '{id, state, html_url}'
```

The response should show `"state": "PENDING"`. Only the reviewer can see it.

### Fallback: Using `position` (diff-relative index)

If `line` + `side` doesn't work (e.g. commenting on a file that wasn't changed by the PR), use the legacy `position` approach. This requires calculating a diff-relative line index:

```bash
# Save diff to a temp file
gh pr diff <N> --repo <OWNER/REPO> > /tmp/pr<N>.diff
```

Then count lines in the diff manually — `position` is the 1-based index of changed lines within each file's diff section (lines starting with `+` or `-`, excluding `---`/`+++`/`@@` headers).

## 2. Show URL and Wait

Show the PENDING review URL. Tell the user they can view it on GitHub's "Files changed" tab.

**Do NOT publish until the user explicitly says "发布" or "publish".**

**If the user wants changes**: Delete the pending review and recreate it. Inline comments on a pending review cannot be edited individually.

```bash
gh api repos/<OWNER/REPO>/pulls/<N>/reviews/<REVIEW_ID> --method DELETE
```

## 3. Publish After Explicit Approval

When the user confirms, submit the review event:

```bash
gh api repos/<OWNER/REPO>/pulls/<N>/reviews/<REVIEW_ID>/events \
  --method POST \
  -f event="<EVENT_TYPE>"
```

**Event type decision:**
- `APPROVE`: Only nits, no blocking issues
- `REQUEST_CHANGES`: Any "must fix" findings
- `COMMENT`: Informational, questions, or suggestions without verdict

Note: `PENDING` is NOT a valid event type for submission. It only exists as the initial state when `event` is omitted during creation.

## 4. Edit a Published Review

To edit a review body after publishing, use GraphQL (REST PATCH may return 404):

```bash
gh api graphql -f query="
mutation {
  updatePullRequestReview(input: {
    pullRequestReviewId: \"<NODE_ID>\",
    body: \"<new body>\"
  }) {
    pullRequestReview { state }
  }
}
"
```

## Common Mistakes (Submission-Specific)

| Mistake | Fix |
|---------|-----|
| Using `event: "PENDING"` in API payload | Omit `event` field entirely to create pending review |
| Using `-f comments[][path]=...` format | Use `--input` with JSON payload instead |
| Using REST PATCH to edit reviews | Use GraphQL `updatePullRequestReview` mutation instead |
| Using `gh pr review --comment` | This creates a NEW review, cannot edit existing ones |
| Using `python -c "..."` for payload building | Write script to temp file first — backticks/quotes in review body break bash |
| Using `/tmp/` on Windows | Use a Windows-compatible temp path (e.g. `C:/tmp/`) |
