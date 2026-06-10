---
name: triage
description: Use when the user wants to quickly understand a complex PR, issue, article, document, web link, discussion, spec, changelog, or unfamiliar topic in plain language; summarize what it is, why it exists, what changed or is being claimed, relevant linked context, risks, and open questions. Match the user's language in the output. For GitHub PRs, use pr-worktree first for isolated local checkout before reading diffs.
---

# Context Triage

## Overview

Turn complicated material into a concise, human-friendly briefing. The input may be a PR, issue, article, web page, design doc, release note, long discussion, or pasted text.

Answer four questions:

1. What is this?
2. Why does it exist or matter?
3. What are the important details, changes, claims, or consequences?
4. What is uncertain, risky, or worth checking next?

Use this as a fast understanding pass before deeper review, implementation, debugging, research, or decision-making.

## Language

Match the user's language in the final triage.

- If the user writes in Chinese, write the triage in Chinese.
- If the user writes in English, write the triage in English.
- If the user mixes languages, use the main language of the user's request.
- Keep code identifiers, file paths, commands, quoted titles, API names, and proper nouns in their original language.
- Do not force a Chinese "简单来说" section for non-Chinese users. Use the equivalent natural label, such as "In plain terms".

## Core Principle

**Infer meaning from multiple signals, never from a single surface.**

Titles, summaries, abstracts, PR bodies, and article intros are claims. Cross-check them against the body, linked context, commits, diffs, issues, comments, citations, dates, authorship, examples, and concrete artifacts.

When sources conflict, prefer primary evidence:

1. Actual artifact or diff
2. Primary source or linked issue/spec
3. Concrete examples, logs, screenshots, or data
4. Author summary
5. Title or headline

## Workflow

### Step 1: Classify the Input

Identify the material type and choose the right evidence path:

| Input | Evidence path |
|---|---|
| GitHub PR | Use the PR workflow below |
| GitHub issue/discussion | Read title, body, labels, comments, linked PRs/issues, reproduction details, and timeline |
| Article or web link | Read the page, then follow only the links needed to understand background, evidence, or consequences |
| Spec/design doc | Read goals, non-goals, architecture, alternatives, risks, and unresolved questions |
| Changelog/release note | Identify user-visible changes, breaking changes, migration needs, and affected components |
| Pasted text | Extract claims, actors, timeline, assumptions, and missing context |

If the user's request is ambiguous, make a reasonable assumption and say what kind of triage you performed.

### Step 2: Gather Context

Fetch enough context to explain the situation accurately.

For web links and articles:

- Open the provided link and identify the author/source, date, main claim, and target audience.
- Follow linked material when it is directly needed to understand the topic, such as original announcements, specs, cited issues, referenced docs, previous posts, or source code.
- Prefer primary sources over secondary summaries.
- Stop following links once additional context stops changing the explanation.
- Note inaccessible, paywalled, deleted, or ambiguous sources instead of guessing.

For local files or docs:

- Read the referenced file first.
- Search nearby docs, tests, examples, or code paths only when they clarify intent or consequences.

For GitHub PRs:

**First, use `pr-worktree` to checkout the PR into an isolated worktree.**

Do not run `gh pr checkout` in the user's current workspace. All local reads, diffs, and tests for this PR should use the PR worktree as `workdir`.

Then run metadata fetches in parallel:

```bash
# PR metadata
gh pr view <N> --json title,body,state,author,labels,createdAt,headRefName,baseRefName,commits,additions,deletions,changedFiles

# CI status
gh pr checks <N> 2>/dev/null || echo "no checks"

# Linked issues (timeline)
gh api repos/<OWNER/REPO>/issues/<N>/timeline --paginate \
  --jq '.[] | select(.event == "cross-referenced" or .event == "connected") | "\(.event) | #\(.source.issue.number // .source.pull_request.number // "") | \(.source.issue.title // "")"'
```

For the diff, use local git with the remote base ref because local base branches may be stale:

```bash
git diff origin/<base-ref>...HEAD
```

If `origin/<base-ref>` does not exist locally, run `git fetch origin <base-ref>` first.

If the user gave a PR URL, extract `owner/repo/number` first, then add `--repo <OWNER/REPO>` to `gh` metadata commands when needed. If no repo is given, infer the repo from the local checkout.

Do not automatically remove the PR worktree after triage. Keep it available for `pr-review`, `pr-fix`, or follow-up exploration.

### Step 3: Infer the Story

Synthesize the evidence into a story a busy human can understand.

Look for:

- The triggering problem, question, or opportunity
- The actor or audience affected
- The concrete change, claim, decision, or event
- The timeline or dependency chain
- The technical, product, operational, or user-facing impact
- The tradeoffs, risks, missing pieces, and unresolved questions

For bug-fix PRs, read the diff like a debugger:

- Is the bug caused by a race condition or timing issue?
- Is it probabilistic or always reproducible?
- What exact state and action sequence trigger it?
- Does the fix add guards, retries, ordering, locking, merge logic, or validation?
- Is the blast radius one user, one feature, or a broader subsystem?

### Step 4: Present the Briefing

Start with a structured summary. Keep it short, but include enough context that the user does not need to open the source immediately.

Use this shape when it fits, translating headings to the user's language:

```markdown
## <Artifact>: <title>

**Source:** <author/site/repo> | **Date:** <date if relevant> | **Status:** <state if relevant>

### Purpose
<1-2 sentences: what this is and why it exists or matters.>

### Key Points
- <important point, change, claim, or finding>
- <important point, change, claim, or finding>

### Context
- <linked issue/spec/post/doc/source and why it matters>
- <timeline or dependency if relevant>

### Impact / Risk
- **Impact:** <who or what is affected>
- **Risk:** <low/medium/high + why>
- **Watchouts:** <uncertainties, missing data, contradictions, or migration concerns>

### Open Questions
- <anything unclear or suspicious>
```

Immediately after the structured summary, add a plain-language translation in the user's language:

> **简单来说** / **In plain terms**: <Explain the core meaning in 2-3 everyday sentences. Avoid repeating the structured summary or leaning on technical terms.>

For PRs, include PR-specific metadata when available:

```markdown
## PR #<N>: <title>

**Author:** @<author> | **<head> -> <base>** | **<N> commits, +<add>/-<del>, <files> files**
**CI:** <pass/fail/pending/no checks>
```

For bug-fix PRs, also include the equivalent of:

> **Bug 性质 / Bug nature**: <race condition, probabilistic trigger, deterministic trigger, and exact trigger condition>
>
> **复现思路 / Reproduction idea**: <how to reproduce on main, with 1-2 concrete approaches such as temporary code injection or natural UI/network throttling>

### Step 5: Offer Useful Next Steps

Offer only the next steps that fit the material:

- For a PR: `pr-review`, `pr-fix`, reproduce the bug on main, or continue investigating a specific subsystem.
- For an article or doc: verify a claim from primary sources, inspect linked code/data, compare against another source, or produce a shorter executive summary.
- For a spec or proposal: review risks, turn it into an implementation plan, or identify missing requirements.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Only summarizing the first page | Follow directly relevant links when they explain background, evidence, or consequences |
| Treating a title/body as truth | Cross-check against concrete artifacts and primary sources |
| Producing a generic summary | Explain why it matters and who is affected |
| Ignoring the user's language | Match the user's language while preserving code, paths, commands, and proper nouns |
| Hiding uncertainty | Call out missing, inaccessible, contradictory, or weak evidence |
| Polluting a repo while reading PRs | Always use `pr-worktree` for isolated PR checkout first |
| Over-reading link chains | Stop when extra links no longer change the explanation |
