---
name: workflow
description: "Nanobot engineering workflows for investigating and explaining problems, designing and changing code or UI, reviewing and maintaining GitHub PRs, verifying behavior, writing technical prose, coordinating bounded work, and Herdr operations. Select a domain, then load only the relevant workflow. Use $workflow with a task or match a clear request; installation does not start work."
---

# Workflow

Read the [runtime contract](references/runtime.md), then choose one domain below for the current request. Read that domain's route and only the matching workflow or playbook. A named method narrows the task; it does not activate the rest of its domain.

| Requested outcome | Read next |
|---|---|
| Understand, triage, explain, recall, or sharpen a task | [Investigate](routes/investigate.md) |
| Design, implement, fix, simplify, improve performance, or refine UI | [Code](routes/code.md) |
| Inspect or maintain a GitHub PR, branch, or worktree | [PR](routes/pr.md) |
| Prove behavior, inspect evidence, or assess a measurement | [Verify](routes/verify.md) |
| Write or revise documentation, comments, or technical prose | [Writing](routes/writing.md) |
| Coordinate parallel work, a longer plan, or a handoff | [Coordinate](routes/coordinate.md) |
| Configure or improve workflows and author verification skills | [Authoring](routes/authoring.md) |
| Open a Herdr pane or explicitly delegate to scode | [Environment](routes/environment.md) |

For a small task, use the shortest matching workflow directly. For a multi-part task, load its additional domains only when those phases are reached. Do not read every route, enumerate all workflows, or load the principles catalog before starting.

## Establish scope

1. Identify the requested result, read/write scope, protected behavior, existing changes, and a falsifiable completion check.
2. Treat investigation, status, review, and planning as read-only unless the request also authorizes edits. Follow any user checkpoint before implementation.
3. Use the selected workflow's concrete helpers and verification path. Resolve relative resources against the document containing the reference. In a leaf workflow, `<skill>` means that document's directory; pass absolute helper paths and an explicit target repository/workdir.
4. Read a linked method or [principle](references/principles.md) only when its decision is relevant. Internal workflow names are file routes, not registered skills or agent types.
5. Report the result, exact artifact, actual checks, evidence, remaining limits, and only the publication actions authorized by the user.

Only `workflow` and `nanobot-gate` are registered by this package. Use `$workflow <task or method>`; old `$pr-review`, `$how`, and `$poteto-mode` names no longer load native skills. Read linked internal documents rather than invoking nonexistent skills.

`$nanobot-gate` is a separate explicit-only entry. Never infer it from a PR, verification, shipping, readiness, or push request, and never interpret `$workflow gate` as its activation.
