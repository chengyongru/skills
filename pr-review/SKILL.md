---
name: pr-review
description: Use when user wants to do a full code review of a PR, submit review comments to GitHub, or get actionable findings on a PR's code quality; use pr-worktree for isolated local checkout before reading or testing PR code
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

### Step 0: Use an Isolated PR Worktree

Before reading changed files or running tests, use `pr-worktree` to ensure the PR is checked out in an isolated worktree. Do not run `gh pr checkout` in the user's current workspace.

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
# Run inside the isolated PR worktree from pr-worktree
# Run project-specific test command
pytest tests/ -x -q --tb=short 2>&1 | tail -30
```

### Step 4: Use Full Audit Scope

Always perform a **full audit**. Do not ask the user to choose a review scope. Even if the user mentions a specific concern, review the PR fully and include that concern in the normal severity-ranked findings when relevant.

**Language: Chat with the user in 中文 (Simplified Chinese). GitHub review body and inline comments must be in English.** Code identifiers, file paths, and technical terms stay in English in both contexts. When presenting findings locally in the conversation, use 中文. When submitting to GitHub, use English.

### Step 5: Present Findings

Structure by severity. Every finding must include file:line and a concrete suggestion:

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
| Switching the user's current branch | Use `pr-worktree` and run review commands in the isolated worktree |
| Only reading diff hunks | Read full files for context |
| Posting comments individually | Use pending review to batch all comments |
| Vague findings ("this could be better") | Every finding needs a concrete suggestion |
| All negative, no positive | Include what the author did well |
| Auto-publishing without user approval | ALWAYS create PENDING, wait for explicit "发布" |
| Writing review body in Chinese when it goes to GitHub | Chat in 中文, GitHub reviews in English |
| Asking what review scope the user wants | Always use full audit scope |
