---
name: triage
description: Use when the user wants to quickly understand a complex PR, issue, article, document, web link, discussion, spec, changelog, or unfamiliar topic in plain language; produce a concise decision brief that explains what it is, why it matters, what changed or is being claimed, the main risks, and the next useful action. Match the user's language. For GitHub PRs, use pr-worktree first for isolated local checkout before reading diffs.
---

# Context Triage

## Goal

Produce a fast decision brief, not a generic summary.

The user should be able to answer, at a glance:

1. What is this?
2. Why should I care?
3. What changed, happened, or is being claimed?
4. What is risky or uncertain?
5. What should I do next?

Default to the perspective of a busy maintainer, reviewer, decision-maker, or operator. Put the decision-useful point first.

## Language

Match the user's language.

- If the user writes Chinese, write natural Chinese.
- If the user writes English, write English.
- If the user mixes languages, use the dominant language of the request.
- Do not mix Chinese and English for ordinary concepts when Chinese is clear.
- Keep code identifiers, file paths, commands, API names, product names, quoted titles, branch names, and proper nouns in their original form.
- Use an English technical term only when translating it would be less precise.

## Evidence

Infer meaning from multiple signals, never from one surface.

Titles, PR bodies, article intros, release notes, and issue summaries are claims. Cross-check them against concrete artifacts:

1. Actual diff, artifact, data, log, screenshot, or reproduction
2. Primary source, linked issue, spec, or official doc
3. Concrete examples and timeline
4. Author summary
5. Title or headline

If evidence conflicts, state the conflict briefly and prefer the concrete artifact.

## Workflow

### 1. Classify

Choose the evidence path:

| Input | Evidence path |
|---|---|
| GitHub PR | Use the PR workflow below |
| GitHub issue/discussion | Read title, body, labels, comments, linked PRs/issues, reproduction details, and timeline |
| Article or web link | Read the page, then follow only links needed to verify background, evidence, or consequences |
| Spec/design doc | Read goals, non-goals, architecture, alternatives, risks, and unresolved questions |
| Changelog/release note | Identify user-visible changes, breaking changes, migration needs, and affected components |
| Pasted text | Extract claims, actors, timeline, assumptions, and missing context |

If the request is ambiguous, make a reasonable assumption and say what you triaged in one short phrase.

### 2. Gather Context

Fetch enough evidence to explain the situation accurately. Stop when extra context no longer changes the conclusion.

For web links:

- Identify source, author, date, main claim, and audience.
- Follow directly relevant primary links only.
- Note inaccessible, deleted, paywalled, or ambiguous sources instead of guessing.

For local files/docs:

- Read the referenced file first.
- Search nearby docs, tests, examples, or code only when it clarifies intent or consequences.

For GitHub PRs:

First use `pr-worktree` to checkout the PR into an isolated worktree. Do not run `gh pr checkout` in the user's current workspace. All local reads, diffs, and tests for this PR should use the PR worktree as `workdir`.

Then fetch metadata in parallel:

```bash
gh pr view <N> --json title,body,state,author,labels,createdAt,headRefName,baseRefName,commits,additions,deletions,changedFiles,mergeable,reviewDecision,statusCheckRollup,isDraft
gh pr checks <N> 2>/dev/null || echo "no checks"
gh api repos/<OWNER/REPO>/issues/<N>/timeline --paginate \
  --jq '.[] | select(.event == "cross-referenced" or .event == "connected") | "\(.event) | #\(.source.issue.number // .source.pull_request.number // "") | \(.source.issue.title // .source.pull_request.title // "")"'
```

Use the remote base for diff:

```bash
git fetch origin <base-ref>
git diff origin/<base-ref>...HEAD
```

Keep the PR worktree after triage for follow-up review or fixes.

### 3. Infer

Do not narrate every fact. Distill the story.

Look for:

- The actual problem, opportunity, or decision
- Who or what is affected
- The smallest accurate description of the change or claim
- The important dependency or timeline
- The review, product, operational, or user impact
- The main risk and the next useful action

For bug-fix PRs, identify:

- Bug nature: race, deterministic trigger, probabilistic trigger, validation gap, ordering issue, stale state, missing guard, etc.
- Exact trigger condition when visible
- Reproduction idea on current main
- Whether the fix narrows the blast radius or changes broader behavior

## Output Contract

Default output must be short, conclusion-first, and easy to scan in one screen.

Use this shape unless the user asks for a different format:

```markdown
**结论：** <artifact type + current decision state + core meaning in 1-2 sentences.>

**它是什么：** <the shortest clear description of the thing.>

**关键变化：** <2-4 bullets or one compact sentence. Mention only changes needed to understand the decision.>

**风险：** <main uncertainty or review concern. Say "低/中/高" only if useful.>

**下一步：** <one concrete next action.>
```

Translate headings naturally for non-Chinese users, for example: `Conclusion`, `What It Is`, `Key Changes`, `Risk`, `Next Step`.

### Output Rules

- Lead with the answer, not metadata.
- Prefer 5 short sections or fewer.
- Avoid long metadata banners. Include author, CI, dates, file counts, labels, and status only when they change the decision.
- Do not add a separate "plain terms" section if the whole answer is already plain.
- Avoid generic phrases like "this is important because it improves maintainability" unless you name the specific boundary, workflow, user, or decision it affects.
- Do not list many files. Name the 1-3 files/modules that matter.
- Do not dump all CI jobs; say "CI 全绿", "CI 失败", "无 CI", or the exact failing job if that matters.
- Do not over-explain process followed. Mention worktree, fetches, or tests only when relevant to trust or next steps.
- Keep bullets flat. Avoid nested bullets.
- For Chinese output, do not use English labels like `Impact / Risk` when `影响 / 风险` or `风险` is clear.

### PR-Specific Emphasis

For PRs, the conclusion should tell a maintainer one of:

- ready to review
- blocked by merge conflict
- blocked by failing CI
- blocked by draft/review process
- likely needs changes before review
- risky despite green CI

Then explain why in one sentence.

For PRs, prioritize:

1. What kind of PR it is: feature, bug fix, refactor, cleanup, test-only, docs, dependency bump
2. What problem it solves
3. What behavior or boundary changes
4. What a reviewer should focus on
5. Whether it is mergeable, draft, reviewed, or blocked

Do not make PR triage a file-by-file changelog.

For bug-fix PRs, add compact lines when evidence supports them:

```markdown
**Bug 性质：** <race/deterministic/probabilistic/etc. + trigger condition.>
**复现思路：** <one practical way to reproduce on main.>
```

## Useful Next Steps

Offer only next steps that fit the material:

- PR: review the named risk area, reproduce the bug, run a targeted test, use `pr-review`, or use `pr-fix`
- Article/doc: verify one key claim from primary evidence, inspect linked code/data, or produce a shorter executive summary
- Spec/proposal: review risks, turn into implementation plan, or identify missing requirements

## Common Mistakes

| Mistake | Fix |
|---|---|
| Starting with metadata | Start with conclusion and decision state |
| Summarizing everything | Select facts that change understanding or action |
| Using mixed Chinese/English labels | Use the user's language; keep only identifiers/proper nouns unchanged |
| Producing a file-by-file PR summary | Explain the change category, intent, risk, and review focus |
| Treating title/body as truth | Cross-check against actual artifact and linked context |
| Hiding uncertainty | State the missing or weak evidence briefly |
| Polluting a repo while reading PRs | Use `pr-worktree` first |
