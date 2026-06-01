---
name: pr-triage
description: Use when user mentions a PR number or URL and wants to quickly understand what it does, why it exists, or what it changes before investing time in a full review
---

# PR Triage

## Overview

Fast PR understanding for maintainers. Parallel-fetch all context, then produce a structured summary answering: **what does this PR do, why does it exist, and what's the risk level?**

Designed to be the first step before `pr-review` or `pr-fix`.

## When to Use

- User shares a PR number/URL and wants to understand it
- User says "what does PR #X do" or "look at this PR"
- Before starting `pr-review` or `pr-fix` on an unfamiliar PR

## Core Principle

**Infer purpose from MULTIPLE sources, never trust a single source.**
PR body may be empty, misleading, or outdated. Cross-reference title, body, linked issues, labels, commit messages, and diff patterns.

## Workflow

### Step 1: Checkout + Parallel Fetch

**First, checkout the PR locally:**

```bash
gh pr checkout <N>
```

This gives you the code on disk so you can inspect files directly with the agent's available file-reading and search tools instead of parsing remote diffs.

**Then, run metadata fetches in parallel:**

```bash
# PR metadata
gh pr view <N> --json title,body,state,author,labels,createdAt,headRefName,baseRefName,commits,additions,deletions,changedFiles

# CI status
gh pr checks <N> 2>/dev/null || echo "no checks"

# Linked issues (timeline)
gh api repos/<OWNER/REPO>/issues/<N>/timeline --paginate \
  --jq '.[] | select(.event == "cross-referenced" or .event == "connected") | "\(.event) | #\(.source.issue.number // .source.pull_request.number // "") | \(.source.issue.title // "")"'
```

**For the diff**, use local git with the **remote** base ref — local base branches may be stale:

```bash
# Diff against the remote base branch (not local, which may be outdated)
git diff origin/<base-ref>...HEAD
```

If `origin/<base-ref>` doesn't exist locally yet, run `git fetch origin <base-ref>` first.

**If user gave a URL**, extract `owner/repo/number` first, then add `--repo <OWNER/REPO>` to the checkout command.

**If no repo given**, `gh pr checkout` infers the repo from the local checkout automatically.

### Step 2: Infer Purpose

Synthesize from all sources:

| Source | What it tells you |
|--------|-------------------|
| PR title | High-level intent |
| PR body | Author's stated purpose (may be wrong/empty) |
| Linked issues | The WHY — what problem this solves |
| Labels | Category: bug, feature, refactor, breaking |
| Commit messages | Granular breakdown of changes |
| Diff patterns | Ground truth — what actually changed |
| File paths | Which subsystems are affected |

**Priority when sources conflict**: diff patterns > linked issues > PR body > title.
The diff never lies; descriptions often misrepresent scope.

**For bug-fix PRs, read the diff like a debugger:**
- Is the bug caused by a **race condition** or **timing issue**? Look for optimistic state, async gaps, or missing guards around concurrent operations.
- Is it **probabilistic**? If the fix adds a guard, retry, or merge logic around async boundaries, it probably doesn't reproduce 100% of the time.
- What is the **trigger condition**? Infer the exact state + action sequence that causes the bug from the diff, not just the PR description.
- What is the **blast radius**? One user, one feature, or systemic?

### Step 3: Present Summary

Start with a **structured summary**, then immediately follow with a **plain-language translation**.

```
## PR #<N>: <title>

**Author:** @<author> | **<head> → <base>** | **<N> commits, +<add>/-<del>, <files> files**
**CI:** <pass/fail/pending>

### Purpose
<1-2 sentences: what this PR does and WHY. Infer from issues + diff, not just the body.>

### Scope
- <subsystem/file>: <what changed>
- <subsystem/file>: <what changed>

### Linked Context
- Fixes #<N>: <issue title> — <one-line summary of the problem>
- Related: #<N>: <title>

### Risk Assessment
- **Size**: <small/medium/large>
- **Breaking**: <yes/no/maybe + what breaks>
- **Risk areas**: <which subsystems, any risky patterns in the diff>

### Open Questions
- <anything unclear or suspicious>
```

**Immediately after the structured summary, add a "说人话" section:**

> **简单来说**：<用 2-3 句话把核心问题和修复方案翻译成日常语言。不要复制上面的技术术语。>

**If the PR is a bug-fix, also include:**

> **Bug 性质**：<是竞态条件/概率触发/必现？触发条件是什么？>
>
> **复现思路**：<如何在 main 上复现？给出 1-2 个具体方法：最简单的临时代码注入法，或者最自然的 UI/网络限速法。>

**After presenting**, offer next steps proactively:
- 要进行代码评审 → `pr-review`
- 要修问题 → `pr-fix`
- 要在 main 上复现这个 Bug → 按上面给的思路操作
- 只是看看 → 用户自行决定是否切回

**Do NOT** automatically switch back to the original branch after triage. Stay on the PR branch so the user can immediately follow up with `pr-review`, `pr-fix`, or further exploration.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping checkout | Always `gh pr checkout` first — local code is easier to explore than remote diffs |
| Only reading PR body | Body may be empty or wrong — always cross-reference diff and issues |
| Summarizing body verbatim | Infer purpose from the diff; body is the author's claim, not the truth |
| Missing linked issues | Issues explain WHY; without them you only understand WHAT |
