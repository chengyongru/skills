# Triage

Produce a one-screen decision brief rather than a comprehensive summary.

## Evidence path

- PR: use [problem-first PR introduction](../../pr/explain/workflow.md) and its response contract instead of the generic brief below. Start with the scenario, failure, and consequence without the change; do not turn an introduction into a correctness review.
- Issue/discussion: inspect body, reproduction, timeline, comments, labels, and linked work.
- Article/link: read the page and directly relevant primary sources.
- Spec/changelog: extract goals, behavior changes, migration needs, risks, and unresolved decisions.
- Pasted text: identify claims, actors, timeline, assumptions, and missing evidence.

Treat titles and author summaries as claims. Prefer actual diffs, artifacts, data, logs, reproductions, specs, and primary sources when evidence conflicts. Stop gathering when more context no longer changes the decision.

## Response

Match the user's language and lead with the conclusion. Default to:

- conclusion and current decision state;
- what it is;
- 2-4 decision-relevant changes;
- main risk or uncertainty;
- one next action.

Include metadata, files, CI jobs, and process details only when they change the decision.
