### Opening a PR

**Prepare a reviewable change; publish only within the user's scope.** Other playbooks may route here for delivery preparation. That is not permission to commit, push, or create a PR. If publication is not authorized, return the local diff, verification, and a proposed title/body instead.

#### Preserve the worktree

Use installed [pr-worktree](../../workflows/pr/worktree/workflow.md) to locate or prepare the branch's registered worktree. Reuse the existing path: one branch maps to one worktree, not one worktree per agent. Inspect branch, head, status, base, and untracked files first. Keep unrelated edits intact. Do not reset, clean, stash, discard files, or recreate a dirty checkout to obtain a convenient starting point. A missing safe write target is a blocker to resolve, not an excuse for a hard reset.

A writing child gets exclusive ownership of that branch/worktree or truly disjoint paths. Stop and reconcile the old writer before assigning a replacement. Child completion does not itself authorize publication.

#### Prepare the diff and evidence

1. Confirm acceptance criteria and the intended base. Inspect the actual diff, including relevant new files, for scope leaks and secrets.
2. Use installed [simplify](../../workflows/code/simplify/workflow.md) for behavior-preserving cleanup and [repo-prose](../../workflows/writing/prose/workflow.md) for repository prose. Keep useful invariants and rationale; do not churn comments merely to satisfy a style ritual. Respect repository commands and the no `ruff format` constraint.
3. Run the narrow checks that prove the changed behavior. Use the matching project verifier, including [nanobot-webui-verify](../../workflows/verify/webui/workflow.md) for nanobot browser flows, or [verify](../../workflows/verify/public/workflow.md). Record exact head or dirty-snapshot state, commands, outcomes, and evidence outside the plugin in `.nanobot-workflows/runs/<run>/`.
4. If commits are authorized, stage only intended paths and keep coherent, ordered commits. Demonstrate failing-then-passing tests locally when appropriate; do not require publishing a broken intermediate commit. Rebase/amend only within granted history-editing scope. Never bypass hooks.

#### Title and body

Follow the repository's convention. Otherwise use `type(scope): subject`, with a short imperative subject and no trailing period. Types include `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, and `perf`.

The body is a one-minute briefing for a reader with the diff. Use these headings in order, dropping empty optional sections:

- `## Why`: problem and approach in one to three sentences.
- `## What changed`: one to three short bullets; name a symbol/path only when it carries the change.
- `## Scope`: what the change covers and deliberately leaves out.
- `## Tradeoffs`: alternatives a reviewer would reasonably ask about, when relevant.
- `## Blast Radius`: affected consumers and the concrete risk.
- `## Verification`: actual commands/scenarios and results, including missing proof. For performance, give a primary before/after number with units and link the full evidence.

Attach screenshots or video when they prove a visible claim. Keep detailed logs, head SHAs, and experiment tables in linked artifacts. Do not label a check successful because it was planned or reported by a child.

#### Authorized publication

Use installed `github` guidance and `gh`. Confirm authentication, repository, remote, branch, base, and current head before mutations. Do not assume another forge CLI or a built-in PR tool exists. Put PR bodies in a data file and pass a body-file argument rather than interpolating untrusted text into shell code. Follow the user's draft/ready choice; if unspecified, report the chosen state and do not mark unfinished work ready.

Push and create/edit the PR only when those remote actions are authorized. A local commit grant is not a push grant. Read the result back with `gh pr view` and report its URL, state, base, and head. A created PR does not start monitoring, publish a review, enable auto-merge, or authorize merging.

For an authorized stack, record the branch/base chain explicitly. The root targets trunk and each child targets its parent branch. Use [pr-worktree](../../workflows/pr/worktree/workflow.md) for each distinct branch and keep one topology writer. Retargeting, rebasing, and force-pushing need their own scope; route authorized landing through Shipping rather than rewriting the chain here.

**Reply:** what is prepared, checks and limitations, local commit/head if made, and any authorized PR URL/state. State the next required authorization instead of silently taking it.
