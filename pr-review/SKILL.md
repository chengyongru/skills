---
name: pr-review
description: Use when user wants to do a full code review of a PR, submit review comments to GitHub, or get actionable findings on a PR's code quality
---

# PR Review

## Overview

Structured code review for PRs. Read changed files in context, produce prioritized findings, optionally submit as a GitHub review with pending review pattern.

**Prerequisite**: Run `pr-triage` first to understand the PR's purpose. Reviews without context miss the point.

## When to Use

- User says "review PR #X" or "do a code review"
- After `pr-triage` when user wants detailed code analysis
- User wants to submit review comments on GitHub

## Workflow

### Step 1: Confirm Context

If `pr-triage` wasn't run this session, do a lightweight context fetch:

```bash
gh pr view <N> --json title,body,headRefName,baseRefName,commits
gh pr diff <N>
```

Ask user if they understand the PR's purpose. If not, suggest `pr-triage` first.

### Step 2: Read Changed Files

For each file in the diff, read the FULL file (not just the diff hunk). Diff shows WHAT changed but you need surrounding context to judge IF the change is correct.

Focus areas by priority:

| Category | What to Look For |
|----------|-----------------|
| Correctness | Logic errors, edge cases, off-by-one, null/undefined |
| Security | Injection, XSS, credential leaks, path traversal |
| API contracts | Breaking changes, inconsistent signatures |
| Error handling | Swallowed exceptions, missing error paths |
| Tests | Missing tests for new behavior, wrong assertions |
| Performance | N+1 queries, unbounded loops, memory leaks |
| Style | Project conventions, naming, dead code |

### Step 3: Run Verification

If CI is failing or the PR touches test-sensitive areas:

```bash
gh pr checkout <N>
# Run project-specific test command
pytest tests/ -x -q --tb=short 2>&1 | tail -30
```

### Step 4: Confirm Review Scope

**Before writing any findings**, ask the user what kind of review they want:

- **Full audit**: Must Fix / Should Fix / Nitpick structure — for PRs about to merge
- **Focused feedback**: Specific concern (e.g. "ask author to split the PR", "check security only") — lightweight, 1-2 key points
- **Quick impression**: High-level observations only — for PRs you're still evaluating

Default to **full audit** only if the user explicitly asked for a thorough review. If the user gives a specific concern (like "too broad, ask them to split"), use **focused feedback** instead of producing a full categorized list.

**Language: Chat with the user in 中文 (Simplified Chinese). GitHub review body and inline comments must be in English.** Code identifiers, file paths, and technical terms stay in English in both contexts. When presenting findings locally in the conversation, use 中文. When submitting to GitHub, use English.

### Step 5: Present Findings

**For full audit**, structure by severity. Every finding must include file:line and a concrete suggestion:

```
## Review: PR #<N>

### Must Fix (阻塞合并)
- **`<file>:<line>`**: <问题描述> — <具体修复建议>

### Should Fix (强烈建议)
- **`<file>:<line>`**: <问题描述>

### Nitpick (可选)
- **`<file>:<line>`**: <建议>

### Positive Notes
- <作者做得好的地方>
```

**For focused feedback**, present 1-3 key points directly without the severity hierarchy.

**Rules for findings:**
- Never flag style issues unless they violate project conventions
- Every "must fix" must explain WHY it's blocking
- Every suggestion must be concrete (show the fix, don't just say "fix this")
- Always include positive notes — reviews should be constructive
- **All natural-language output must be in 简体中文** (local presentation only; GitHub reviews in English)

### Step 6: Ask to Submit

After presenting findings, ask the user: "要不要以 PENDING review 发布到 GitHub？"

If yes, follow **github-submission.md** for the mechanical steps. If no, stop here.

## Code Suggestion Format

When suggesting code changes in review comments, use GitHub's suggestion syntax:

````markdown
```suggestion
<the suggested code>
```
````

This lets the author apply the suggestion with one click.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Reviewing without understanding purpose | Run `pr-triage` first |
| Only reading diff hunks | Read full files for context |
| Posting comments individually | Use pending review to batch all comments |
| Vague findings ("this could be better") | Every finding needs a concrete suggestion |
| All negative, no positive | Include what the author did well |
| Auto-publishing without user approval | ALWAYS create PENDING, wait for explicit "发布" |
| Writing review body in Chinese when it goes to GitHub | Chat in 中文, GitHub reviews in English |
| Producing full audit when user has a specific concern | Ask about review scope first (Step 4) — use focused feedback for targeted requests |
