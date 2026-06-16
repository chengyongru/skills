---
name: pr-review
description: Use when user wants to do a full maintainer-quality review of a PR, identify blockers or recommend rejection/closure, label the PR using existing repository labels, submit review comments to GitHub, or get actionable findings on correctness, architecture, maintainability, focus, tests, and code quality; produce PR review findings in professional English; never approve PRs; disclose GitHub reviews as nanobot automated reviews; use pr-worktree for isolated local checkout before reading or testing PR code
---

# PR Review

## Overview

Structured maintainer-quality code review for PRs. Read changed files in context, verify the PR's stated behavior against implementation and tests, label the PR with appropriate existing repository labels, identify whether the PR has blockers, should be changed, split, or rejected, produce prioritized findings, and optionally submit as a GitHub review with pending review pattern.

**Authority boundary**: This skill must never approve a PR or submit a GitHub `APPROVE` review. If no blocking findings are found, say "No blocking findings found" and leave the final merge decision to a human maintainer.

**Identity boundary**: Any review submitted to GitHub must clearly state that it is an automated review by nanobot, not a human maintainer review. Do not write phrasing that implies a human personally reviewed or approved the PR.

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
gh pr view <N> --json labels
gh label list --limit 200
git diff --stat origin/<base>...HEAD
git diff --name-only origin/<base>...HEAD
```

Infer the PR's purpose from title, body, commit history, touched files, and tests. Ask only if the purpose remains ambiguous enough that a review would be speculative.

Before reading code, write down the PR's claimed behavioral contract:

- What behavior is supposed to become stricter, looser, faster, or safer?
- Which paths are in scope and explicitly out of scope?
- What must never happen after this PR?
- What compatibility behavior is intentionally preserved?

Then decide whether the PR has a valid premise before spending the full review budget:

- What real user, maintainer, security, compatibility, or operational problem is this PR trying to solve?
- Is the motivating scenario reachable in the product as shipped, or only hypothetical/dead/test-only code?
- Is the fix proportional to the problem, or does it add broad machinery for a narrow or impossible case?
- Does the PR look accidental, generated, stale, duplicate, or unrelated to the project's current direction?

If the premise is invalid, still verify enough evidence to be fair, but do not invent a patch plan for the author. The right review result may be "close this PR" or "reject this approach", not "please make these changes".

### Step 1.5: Build the Maintainer Review Model

Read repository-local review policy before judging design. Prefer files such as `AGENTS.md`, `.agent/design.md`, `.agent/security.md`, `.agent/gotchas.md`, `CONTRIBUTING.md`, and nearby package docs when present.

From those docs and the changed-file list, identify:

- **Expected ownership layer**: where this kind of behavior belongs.
- **Critical paths**: files where changes must be minimal and strongly justified.
- **Extension points**: registries, adapters, hooks, plugins, coordinators, templates, or config schemas the PR should use.
- **Dependency direction**: which layers are allowed to know about each other.
- **Existing canonical helpers**: parsing, validation, security, persistence, transport, UI state, or error-handling utilities that should not be bypassed.

Use this model to review the shape of the PR, not only whether the code runs. A PR can be functionally correct and still unacceptable if it puts behavior in the wrong layer, creates circular ownership, bypasses a required boundary, or makes the codebase harder to maintain for no real benefit.

### Step 1.6: Label the PR

During review, inspect the repository's current labels and the PR's existing labels:

```bash
gh label list --limit 200
gh pr view <N> --json labels
```

Choose appropriate labels from labels that already exist in the repository. Do not create new labels, rename labels, remove labels, or replace human-maintainer labels unless the user explicitly asks.

Prefer one intent/status label plus one affected-area label when the repository's existing label taxonomy supports that distinction. Add up to three labels total only when each label adds real routing value.

Infer the repository's taxonomy from label names and descriptions. Common patterns include:

- intent/status labels, if present: bug, regression, enhancement, documentation, refactor, invalid, duplicate, stale, question
- affected-area labels, if present: frontend, backend, api, cli, docs, tests, ci, provider, integration, security

Apply labels with:

```bash
gh pr edit <N> --add-label "<label>"
```

If labels are ambiguous, do not guess an overly specific label; use a broader existing label or report that no label was applied. In the final local response, mention which labels were added or why labeling was skipped.

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
| Premise | No real problem, unreachable scenario, accidental/stale/duplicate PR, disproportionate solution |
| Architecture | Wrong ownership layer, core-path pollution, circular dependencies, bypassed extension points |
| Correctness | Logic errors, edge cases, off-by-one, null/undefined |
| Security | Injection, XSS, credential leaks, path traversal |
| API contracts | Breaking changes, inconsistent signatures |
| Error handling | Swallowed exceptions, missing error paths |
| Tests | Missing tests for new behavior, wrong assertions |
| Performance | N+1 queries, unbounded loops, memory leaks |
| Focus / Scope | Multiple unrelated features, unnecessary churn, PR body drifting from code |
| Maintainability | needless abstractions, low-value wrappers, poor reuse of canonical helpers, technical debt |
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

**Language: Chat around the review in the same language the user used for the request. The actual PR review artifact, including findings, verdict, GitHub review body, and inline comments, must be in professional English.** Code identifiers, file paths, and technical terms stay in their original language. When submitting to GitHub, begin the body with: `Automated PR review by nanobot. This is not a human maintainer review or approval.`

### Step 4.5: Apply Maintainer Review and Rejection Gates

Before presenting findings, explicitly decide whether the PR has blockers or should be rejected/closed:

- **Premise gate**: The PR solves a real, reachable, worthwhile problem. If it appears accidental, duplicate, stale, or aimed at an impossible/non-product path, recommend closing or rejecting rather than asking for edits.
- **Correctness gate**: The implementation satisfies the claimed contract across all relevant entrypoints.
- **Safety gate**: Invalid or rejected operations cannot be silently transformed into a different successful operation.
- **Architecture boundary gate**: Behavior lives in the correct ownership layer and uses the intended extension point. UI/channel/provider/tool-specific behavior must not leak into unrelated core paths.
- **Dependency direction gate**: The PR does not introduce circular dependencies, reverse ownership, or inappropriate knowledge between layers.
- **Reuse/locality gate**: The PR reuses canonical helpers and established local patterns where that reduces risk. Do not demand abstraction just to remove acceptable local duplication.
- **Core-path budget gate**: Changes to critical paths are minimal, general, and justified by the PR's contract.
- **Focus gate**: The PR has one coherent theme. Unrelated features, policy changes, or refactors should be split.
- **Minimum diff gate**: Pure churn, style-only renames, wrapper functions without value, and broad rewrites should be challenged unless they reduce real risk or complexity.
- **Documentation gate**: PR body, comments, and tests describe the actual semantics. Ambiguous wording that could mislead maintainers is at least a nit; if it changes user expectations, raise it higher.
- **Verification gate**: CI and local checks cover the risky behavior, and any residual risk is stated.

Do not convert passing gates into approval. A clean review means "no blocking findings found in this pass", not "approved to merge".

Not every failed gate should produce a fix list. Use this calibration:

- **Reject / Close**: invalid premise, accidental PR, unreachable problem, duplicate/stale work, or a solution whose complexity is not worth carrying.
- **Request changes**: valid problem, but implementation violates correctness, safety, architecture, dependency direction, or reviewability gates.
- **Comment-only**: non-blocking concerns, unclear tradeoffs, or residual risk the maintainer should consider.
- **No blocking findings**: gates pass based on the evidence reviewed. Do not call this approval.

### Step 5: Present Findings

Structure the PR review artifact in professional English by severity. Every finding must include file:line and a concrete suggestion:

```
## Review: PR #<N>

### Must Fix
- **`<file>:<line>`**: <issue description> — <concrete suggested fix>

### Should Fix
- **`<file>:<line>`**: <issue description>

### Nitpick
- **`<file>:<line>`**: <suggestion>

### Positive Notes
- <what the author did well>

### Review Verdict
- <No blocking findings / Request changes / Comment-only / Reject or close> — <one-sentence rationale>
```

**Rules for findings:**
- Never flag style issues unless they violate project conventions
- Every "must fix" must explain WHY it's blocking
- Every suggestion must be concrete (show the fix, don't just say "fix this")
- Always include positive notes — reviews should be constructive
- Surrounding conversation with the user must use the user's language. The review findings, verdict, GitHub body, and inline comments must use professional English.
- If there are no findings, say that clearly, then state remaining test gaps or residual risk.

**Severity calibration:**
- **Must Fix**: wrong operation could execute, data/security boundary is weakened, public contract breaks, PR's central claim is false, or CI/merge state blocks safe merge.
- **Should Fix**: likely bug, missing important test, ambiguous API/config semantics, unnecessary complexity in a risky path, architectural boundary drift, poor reuse of canonical helpers, or PR scope is too broad but not unsafe.
- **Nitpick**: PR body wording, small minimum-diff cleanup, local naming/style churn, or non-blocking maintainability issue.
- **Reject / Close**: accidental PR, no real reachable problem, duplicate/stale work, impossible scenario, or the proposed complexity is fundamentally not worth merging. Do not provide a long implementation checklist for these; explain the evidence and recommend closing.

### Step 6: Ask to Submit

After presenting findings, ask the user in their language whether to create or publish a PENDING review on GitHub.

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
| Skipping labels | Read current repository labels and apply suitable existing labels during review |
| Creating labels during review | Use only existing labels unless the user explicitly asks to create or rename labels |
| Over-labeling | Add only labels that materially help classify or route the PR |
| Vague findings ("this could be better") | Every finding needs a concrete suggestion |
| All negative, no positive | Include what the author did well |
| Auto-publishing without user approval | ALWAYS create PENDING, wait for explicit "发布" |
| Approving a PR | Never approve PRs; report "No blocking findings" and leave approval to a human maintainer |
| Implying a human reviewed the PR | Start every GitHub review body with the nanobot automated-review disclosure |
| Forcing Chinese in local chat | Match the user's language for local conversation |
| Localizing the review findings themselves | Keep the actual PR review artifact in professional English |
| Writing the GitHub review in the wrong language | GitHub review body and inline comments must be in professional English |
| Asking what review scope the user wants | Always use full audit scope |
| Trusting CI alone | Derive adversarial checks from the PR's own contract |
| Ignoring PR body drift | Compare PR description, tests, and implementation semantics |
| Reviewing only the new helper | Search all call sites and alternate entrypoints |
| Accepting broad PRs | Apply the focus gate and recommend splitting unrelated work |
| Treating every PR as salvageable | Apply the premise gate; invalid or accidental PRs should be closed, not rewritten |
| Treating working code as merge approval | Also judge architecture, dependency direction, ownership, and long-term maintenance cost; still do not approve |
| Demanding abstraction everywhere | Reuse canonical helpers, but respect repo-local guidance that favors local duplication in some adapters |
| Overweighting style | Prefer minimum diff; raise style only when it affects lint or maintainability |
