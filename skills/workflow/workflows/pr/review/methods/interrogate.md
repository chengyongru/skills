# Interrogate

Use two fresh reviewer tasks to challenge code changes and produce a synthesized verdict. Separate contexts can expose different evidence, but children inherit the configured model and may share blind spots. If cross-model acceptance is explicitly required, report it blocked. Do not auto-apply changes or publish a review. For a GitHub PR review, follow installed [pr-review](../workflow.md) first and use this only as a supplemental local lens.

## Step 1, Scope

Retain the parent review's exact scope, base, and target SHA. For a standalone request, resolve the named files/diff or the branch's merge base and target SHA once. Include uncommitted changes only when they belong to the requested scope, and identify them separately from committed sources. Do not substitute a moving `HEAD` or the full branch for a narrower supplied snapshot.

Package that diff or file content with the surrounding context paths reviewers need. A finding must refer to the same snapshot as its evidence.

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

## Output

For a PR, follow the parent [PR review output contract](../workflow.md). The buckets above are internal triage, not mandatory report sections. For a standalone review, lead with actionable findings or say none were found; include only risks or evidence gaps that could change the recommendation.

Distinguish source-based findings from reproduced failures. A decisive source trace can support a finding without a run; a read-only pass cannot claim runtime verification. When reproduction is authorized and needed to settle a claim, verify it at the scoped snapshot before calling it reproduced.

Briefly identify the use or absence of fresh reviewer contexts and the same-model limitation. Omit empty sections. Include intent, reviewer-by-reviewer breakdowns, dismissed items, or an agreement map only when the user asks for the full audit.
