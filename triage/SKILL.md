---
name: triage
description: Produce a concise decision brief for a complex PR, issue, article, document, web link, discussion, spec, changelog, or unfamiliar topic. Explain what it is, why it matters, the key change or claim, main risk, and next action in the user's language. Use pr-worktree first for GitHub PRs.
---

# Triage

Produce a one-screen decision brief rather than a comprehensive summary.

## Evidence path

- PR: prepare an isolated checkout with `pr-worktree`, then inspect metadata, remote-base diff, CI, linked issues, and the smallest relevant code/test context.
- Issue/discussion: inspect body, reproduction, timeline, comments, labels, and linked work.
- Article/link: read the page and directly relevant primary sources.
- Spec/changelog: extract goals, behavior changes, migration needs, risks, and unresolved decisions.
- Pasted text: identify claims, actors, timeline, assumptions, and missing evidence.

Treat titles and author summaries as claims. Prefer actual diffs, artifacts, data, logs, reproductions, specs, and primary sources when evidence conflicts. Stop gathering when more context no longer changes the decision.

## PR judgment

Identify the PR type, problem, changed boundary, affected user or maintainer, merge/process state, main review risk, and next useful action. For bug fixes, include the trigger and a practical reproduction idea when evidence supports them.

Use `pr-worktree` as the workdir for all local reads and keep it for likely review/fix follow-up.

## Response

Match the user's language and lead with the conclusion. Default to:

- conclusion and current decision state;
- what it is;
- 2-4 decision-relevant changes;
- main risk or uncertainty;
- one next action.

Include metadata, files, CI jobs, and process details only when they change the decision.
