# Interrogate

Use two fresh reviewer tasks to challenge code changes and produce a synthesized verdict. Separate contexts can expose different evidence, but children inherit the configured model and may share blind spots. If cross-model acceptance is explicitly required, report it blocked. Do not auto-apply changes or publish a review. For a GitHub PR review, follow installed [pr-review](../workflow.md) first and use this only as a supplemental local lens.

## Step 1, Scope

Identify what to review from context:

- If the user points at specific files or a diff, use that.
- If on a feature branch, run `git diff main...HEAD` (or the appropriate base branch) for the full changeset.
- If the user's message references recent work, gather the relevant files.

Package the diff or file contents with any surrounding context files the reviewers need to understand the code.

## Step 2, Intent

Before spawning reviewers, state the intent in one clear paragraph from the user's message, commit messages, the PR description if one exists, and the code. If you're unsure about the intent, ask the user before proceeding.

## Step 3, Spawn Reviewers

Read `references/reviewer-prompt.md`. Give Reviewer A and Reviewer B the same intent, exact diff/head, surrounding context paths, `references/rubric.md`, and `references/code-quality-review.md`. Both apply the full relevant rubric. Do not show either the other's findings before its first report.

Create bounded `subagent` tasks with labels and `wait=false`, keeping returned `task_id` values. Each task explicitly prohibits edits, commits, service launches, ticket changes, and publication. Await completion notifications; inspect a known ID with `check` when needed. If delegation is unavailable or prohibited, do the review directly and report the missing fresh views. Do not create a PR or edit package defaults to compensate for unavailable capabilities.

## Step 4, Synthesize

Parse every reviewer's findings. Merge findings that describe the same issue differently and retain reviewer labels. Check the execution path and evidence for every actionable finding, including singletons. Same-model agreement is not independent confirmation. Note disagreements and resolve them from the code and task constraints rather than voting.

## Step 5, Lead Judgment

You are the lead reviewer, a pragmatic senior engineer, not a neutral aggregator. Read `references/lead-judgment.md` for the full framework. Put every finding in one of four buckets, with the reviewer(s) that raised it and a one-line evidence-based rationale.

- **Act on**. Real issues affecting correctness, security, or maintainability given the actual goals. They would block a real PR.
- **Consider**. Legitimate, but you're not sure they outweigh the cost of addressing them now. Worth the user's attention.
- **Noted**. Technically valid but not actionable. Context-dependent, premature optimization, or low-impact at this stage.
- **Dismissed**. Wrong, nitpicky, or missing context, with a brief reason.

## Output Format

### Intent
> [The stated intent paragraph from Step 2]

### Reviewers
- Reviewer [label]: [scope, N findings, completion/limitation] (one bullet per reviewer). State that views used the same runtime-configured model; name it only if actually known.

### Act On
[Each: description, which reviewers raised it, reachable evidence, why it matters.]

### Consider
[Each: description, which reviewers raised it, the tradeoff.]

### Noted
[Brief list.]

### Dismissed
[Each with a brief rationale.]

### Agreement Map
[Where reviewers agreed and diverged, evidence resolving disagreements, and the same-model limitation. Agreement alone does not establish correctness.]
