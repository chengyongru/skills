---
name: triage
description: Produce a concise decision brief for a complex PR, issue, article, document, web link, discussion, spec, changelog, or unfamiliar topic. Explain what it is, why it matters, the key change or claim, main risk, and next action in the user's language.
---

# Triage

Produce a one-screen decision brief rather than a comprehensive summary.

## Evidence path

- PR: inspect remote metadata, the base diff, CI, linked issues, and only the smallest context that can change the decision. Keep triage remote-only; hand off to `pr-review`, `pr-fix`, or `verify` when a local checkout or execution is needed.
- Issue/discussion: inspect body, reproduction, timeline, comments, labels, and linked work.
- Article/link: read the page and directly relevant primary sources.
- Spec/changelog: extract goals, behavior changes, migration needs, risks, and unresolved decisions.
- Pasted text: identify claims, actors, timeline, assumptions, and missing evidence.

Treat titles and author summaries as claims. Prefer actual diffs, artifacts, data, logs, reproductions, specs, and primary sources when evidence conflicts. Stop gathering when more context no longer changes the decision.

## PR judgment

Identify the PR type, problem, changed boundary, affected user or maintainer, merge/process state, main review risk, and next useful action. For bug fixes, include the trigger and a practical reproduction idea when evidence supports them.

Keep the triage result independent of a local worktree. Name the next local workflow when the decision requires code inspection, testing, or an edit.

## Response

Match the user's language and lead with the conclusion. Default to:

- conclusion and current decision state;
- what it is;
- 2-4 decision-relevant changes;
- main risk or uncertainty;
- one next action.

Include metadata, files, CI jobs, and process details only when they change the decision.
