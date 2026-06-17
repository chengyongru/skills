---
name: pr-audit-sweep
description: Use when Codex needs to run one GitHub PR audit sweep over open PRs; audits each PR at most once by default, applies suitable existing labels, delegates deep review to pr-review, records audit state with a script, and produces a digest without approving, merging, closing, or repeatedly posting on PRs.
---

# PR Audit Sweep

## Overview

Run one audit pass over open GitHub PRs. This skill selects PRs, enforces idempotency, calls `triage` and `pr-review` for each selected PR, applies high-confidence existing labels, and reports a digest.

It does not replace `pr-review`. Use `pr-review` for the actual maintainer-quality review of one PR. Use this skill when the task is "scan the PR queue" or "run a PR audit sweep".

Scheduling, recurrence, and trigger frequency are outside this skill. If an external task runner invokes this skill repeatedly, this skill still performs only one bounded sweep each time.

## Core Policy

- Audit each PR at most once by default, keyed by PR number.
- Do not automatically re-audit a PR when new commits are pushed after the first Agent review. Those follow-up changes are for the human maintainer to handle unless the user explicitly asks the Agent to review that PR again.
- Re-audit only on an explicit user request, using `--force` or by clearing that PR's state entry as part of that request.
- Never approve PRs.
- Never merge, close, delete branches, or remove human labels.
- Use only labels that already exist in the repository.
- Default to labels plus digest. Publish public GitHub review comments only if the task/policy explicitly allows it.
- If publishing a GitHub review, use `pr-review`'s pending review flow and nanobot identity disclosure.

## State Script

Use `scripts/pr_audit_state.py` for all audit-state file operations. Do not hand-edit `.nanobot/pr-audit-state.json`.

Default state path:

```text
.nanobot/pr-audit-state.json
```

Common commands:

```bash
# Policy management
python <skill>/scripts/pr_audit_state.py set-policy --created-after "<ISO datetime>"
python <skill>/scripts/pr_audit_state.py policy

# Discovery: get all pending PRs in one call
python <skill>/scripts/pr_audit_state.py list-pending --repo owner/name

# Per-PR state transitions
python <skill>/scripts/pr_audit_state.py should-audit --pr 123 --created-at "<ISO>"
python <skill>/scripts/pr_audit_state.py mark-started --pr 123 --head-sha abc123 --title "Fix bug"
python <skill>/scripts/pr_audit_state.py mark-reviewed --pr 123 --verdict "Clean" --label enhancement
python <skill>/scripts/pr_audit_state.py mark-skipped --pr 123 --reason "draft"
python <skill>/scripts/pr_audit_state.py mark-failed --pr 123 --reason "checkout error"
python <skill>/scripts/pr_audit_state.py list
```

Use `--state <path>` only when the repository policy specifies a different location.

## Workflow

### Step 1: Establish Policy and Budget

Read repository-local policy if present, such as:

- `.github/nanobot-pr-audit.md`
- `.agent/pr-audit.md`
- `AGENTS.md`
- `CONTRIBUTING.md`

Extract:

- maximum PRs to audit this run
- optional audit cutoff such as `created_after` or `min_pr_number`
- whether public GitHub comments are allowed
- whether `REQUEST_CHANGES` is allowed
- labels that should or should not be automated
- paths requiring deeper verification
- skip rules for draft, bot-authored, stale, or external PRs

If no policy exists, use safe defaults:

- audit at most 3 PRs per run
- skip drafts
- label only when high confidence
- publish no public review unless explicitly requested
- produce a digest in the final response

If the invocation or repository policy supplies an audit cutoff, store it through the state script before filtering PRs:

```bash
python <skill>/scripts/pr_audit_state.py set-policy --created-after "<ISO datetime>"
python <skill>/scripts/pr_audit_state.py set-policy --min-pr-number <N>
```

Use `created_after` when possible because it directly represents "do not audit PRs created before automation started." Use `min_pr_number` only when that is the available policy input. Do not invent or hardcode a cutoff inside the skill; it must come from the user, the external task configuration, or repository policy.

### Step 2: Discover Pending PRs and Labels

Get the list of PRs that need auditing in a single call:

```bash
python <skill>/scripts/pr_audit_state.py list-pending --repo owner/name
```

This handles all filtering internally: reads policy `created_after` from state, fetches open PRs from GitHub, skips drafts and pre-cutoff PRs, and excludes already-audited entries. Returns only `{"pending": [...]}` — each entry includes `pr`, `title`, `author`, `head_sha`, `url`, `created_at`.

When there are no pending PRs, the output is `{"pending": []}` — silent exit.

Also fetch the repository's labels for this run:

```bash
gh label list --repo owner/name --limit 200
```

Infer the repository's taxonomy from current label names and descriptions; do not assume labels from another repository.

### Step 3: Audit One PR at a Time

For each selected PR:

1. Mark it started:

   ```bash
   python <skill>/scripts/pr_audit_state.py mark-started --pr <N> --head-sha <SHA> --created-at "<createdAt>" --title "<title>"
   ```

2. Run `triage` to understand purpose.
3. Run `pr-review` for the actual review, labels, and optional pending review creation.
4. Run `verify` only when the PR risk justifies black-box checks and the budget allows it.
5. Mark the final outcome:

   ```bash
   python <skill>/scripts/pr_audit_state.py mark-reviewed --pr <N> --head-sha <SHA> --created-at "<createdAt>" --verdict "<verdict>" --label "<label>"
   ```

If the PR is skipped by policy after inspection, use `mark-skipped`. If audit fails due to environment, permissions, checkout, or tests, use `mark-failed` with a concise reason. Failed PRs are still considered attempted and should not loop forever across repeated invocations; retry only when explicitly forced.

### Step 4: Produce Digest

The final response should be in the user's language and include:

- PRs audited
- PRs skipped and why
- labels applied
- PRs needing human attention
- suspected reject/close candidates
- verification performed or skipped
- failures that need infrastructure attention

The review artifact itself, if shown or published, must remain in professional English because `pr-review` requires that.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Re-auditing a PR after every new commit | Default to once per PR number; force retry only when explicitly requested |
| Auditing PRs that existed before automation was enabled | Configure `created_after` or `min_pr_number` in audit state from user/task/policy input |
| Hardcoding the start cutoff in the skill | Store the cutoff in audit state with `set-policy` |
| Handling author follow-up changes automatically | Leave post-review author changes to the human maintainer unless the user explicitly asks for another Agent review |
| Hand-editing audit state JSON | Use `scripts/pr_audit_state.py` |
| Creating labels | Use only existing labels |
| Publishing public reviews by default | Default to digest-only unless policy allows public comments |
| Approving PRs | Never submit `APPROVE`; `pr-review` can only comment or request changes |
| Running too many PRs in one invocation | Apply a run budget and continue next time |
| Letting failed audits loop forever | Mark failed attempts and require explicit retry |
| Calling `should-audit` per PR in a loop | Use `list-pending --repo owner/name` to get pending PRs in one call |
