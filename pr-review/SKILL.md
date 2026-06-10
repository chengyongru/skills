---
name: pr-review
description: Use when user wants to do a full maintainer-quality review of a PR, decide whether a PR is merge-ready, submit review comments to GitHub, or get actionable findings on correctness, focus, tests, and code quality; use pr-worktree for isolated local checkout before reading or testing PR code
---

# PR Review

## Overview

Structured maintainer-quality code review for PRs. Read changed files in context, verify the PR's stated behavior against implementation and tests, judge merge readiness, produce prioritized findings, and optionally submit as a GitHub review with pending review pattern.

**Prerequisite**: Run `triage` first to understand the PR's purpose. Reviews without context miss the point.

## When to Use

- User says "review PR #X", "do a code review", or asks whether a PR is merge-ready
- After `triage` when user wants detailed code analysis of a PR
- User wants to submit review comments on GitHub

## Workflow

### Step 0: Use an Isolated PR Worktree

Before reading changed files or running tests, use `pr-worktree` to ensure the PR is checked out in an isolated worktree. Do not run `gh pr checkout` in the user's current workspace.

### Step 1: Confirm Context

If `triage` was not run for this PR in this session, do a lightweight context fetch:

```bash
gh pr view <N> --json title,body,headRefName,baseRefName,commits,files,mergeable,reviewDecision,statusCheckRollup
git diff --stat origin/<base>...HEAD
git diff --name-only origin/<base>...HEAD
```

Infer the PR's purpose from title, body, commit history, touched files, and tests. Ask only if the purpose remains ambiguous enough that a review would be speculative.

Before reading code, write down the PR's claimed behavioral contract:

- What behavior is supposed to become stricter, looser, faster, or safer?
- Which paths are in scope and explicitly out of scope?
- What must never happen after this PR?
- What compatibility behavior is intentionally preserved?

### Step 2: Read Changed Files

For each file in the diff, read the FULL file (not just the diff hunk). Diff shows WHAT changed but you need surrounding context to judge IF the change is correct.

Use `rg` to find all relevant call sites and sibling implementations. Do not assume a helper is only used where the diff shows it.

For PRs that change validation, parsing, permissions, tool execution, provider adapters, gateways, storage, or other boundaries, build a small boundary matrix before judging correctness. Include dimensions such as:

- fresh input vs historical replay/migration
- valid input vs malformed/array/scalar/null/empty input
- public API vs internal direct call
- streaming vs non-streaming path
- successful execution vs rejected/error path
- telemetry/result fields that should reflect only successful work

Actively look for a counterexample to the PR's central claim. A green test suite is not enough if a simple untested scalar, null, path, missing field, duplicate ID, or alternate entrypoint would violate the intended contract.

Focus areas by priority:

| Category | What to Look For |
|----------|-----------------|
| Correctness | Logic errors, edge cases, off-by-one, null/undefined |
| Security | Injection, XSS, credential leaks, path traversal |
| API contracts | Breaking changes, inconsistent signatures |
| Error handling | Swallowed exceptions, missing error paths |
| Tests | Missing tests for new behavior, wrong assertions |
| Performance | N+1 queries, unbounded loops, memory leaks |
| Focus / Scope | Multiple unrelated features, unnecessary churn, PR body drifting from code |
| Style | Project conventions, naming, dead code, only when it affects maintainability or lint |

### Step 3: Run Verification

Always check mergeability and CI status from `gh pr view`. If CI is failing, blocked, or stale, mention it explicitly.

Run verification when the PR touches code paths where behavior matters, not only when CI is failing:

```bash
# Run inside the isolated PR worktree from pr-worktree
# Prefer focused tests first; broaden when shared contracts are touched.
pytest tests/ -x -q --tb=short 2>&1 | tail -30
```

Design at least one adversarial or black-box check from the PR's claimed invariant when feasible. Examples:

- If invalid input must not execute, probe malformed JSON, arrays, scalars, `"null"`, empty strings, missing fields, and direct registry/API calls.
- If a suggestion/hint is added, verify the suggested action is not executed unless explicitly intended.
- If a field reports successful work, verify rejected/failed attempts do not pollute it.
- If a compatibility/replay path remains permissive, verify that permissiveness is not reused for fresh execution.

### Step 4: Use Full Audit Scope

Always perform a **full audit**. Do not ask the user to choose a review scope. Even if the user mentions a specific concern, review the PR fully and include that concern in the normal severity-ranked findings when relevant.

**Language: Chat with the user in 中文 (Simplified Chinese). GitHub review body and inline comments must be in English.** Code identifiers, file paths, and technical terms stay in English in both contexts. When presenting findings locally in the conversation, use 中文. When submitting to GitHub, use English.

### Step 4.5: Apply Maintainer Merge Gates

Before presenting findings, explicitly decide whether the PR is suitable to merge:

- **Correctness gate**: The implementation satisfies the claimed contract across all relevant entrypoints.
- **Safety gate**: Invalid or rejected operations cannot be silently transformed into a different successful operation.
- **Focus gate**: The PR has one coherent theme. Unrelated features, policy changes, or refactors should be split.
- **Minimum diff gate**: Pure churn, style-only renames, wrapper functions without value, and broad rewrites should be challenged unless they reduce real risk or complexity.
- **Documentation gate**: PR body, comments, and tests describe the actual semantics. Ambiguous wording that could mislead maintainers is at least a nit; if it changes user expectations, raise it higher.
- **Verification gate**: CI and local checks cover the risky behavior, and any residual risk is stated.

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

### Merge Readiness
- <Approve / Request changes / Comment-only> — <one-sentence rationale>
```

**Rules for findings:**
- Never flag style issues unless they violate project conventions
- Every "must fix" must explain WHY it's blocking
- Every suggestion must be concrete (show the fix, don't just say "fix this")
- Always include positive notes — reviews should be constructive
- **All natural-language output must be in 简体中文** (local presentation only; GitHub reviews in English)
- If there are no findings, say that clearly, then state remaining test gaps or residual risk.

**Severity calibration:**
- **Must Fix**: wrong operation could execute, data/security boundary is weakened, public contract breaks, PR's central claim is false, or CI/merge state blocks safe merge.
- **Should Fix**: likely bug, missing important test, ambiguous API/config semantics, unnecessary complexity in a risky path, or PR scope is too broad but not unsafe.
- **Nitpick**: PR body wording, small minimum-diff cleanup, local naming/style churn, or non-blocking maintainability issue.

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
| Reviewing without understanding purpose | Run `triage` first |
| Switching the user's current branch | Use `pr-worktree` and run review commands in the isolated worktree |
| Only reading diff hunks | Read full files for context |
| Posting comments individually | Use pending review to batch all comments |
| Vague findings ("this could be better") | Every finding needs a concrete suggestion |
| All negative, no positive | Include what the author did well |
| Auto-publishing without user approval | ALWAYS create PENDING, wait for explicit "发布" |
| Writing review body in Chinese when it goes to GitHub | Chat in 中文, GitHub reviews in English |
| Asking what review scope the user wants | Always use full audit scope |
| Trusting CI alone | Derive adversarial checks from the PR's own contract |
| Ignoring PR body drift | Compare PR description, tests, and implementation semantics |
| Reviewing only the new helper | Search all call sites and alternate entrypoints |
| Accepting broad PRs | Apply the focus gate and recommend splitting unrelated work |
| Overweighting style | Prefer minimum diff; raise style only when it affects lint or maintainability |
