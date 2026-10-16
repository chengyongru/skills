# GitHub PRs and worktrees

Choose the authorized operation; a status question is not permission to repair or publish. Confirm the repository and current head. Keep the requested snapshot separate from dirty working files.

| Operation | Workflow or playbook |
|---|---|
| Explain a PR before local review | [Remote-only triage](../workflows/investigate/triage/workflow.md) |
| Check head, CI, reviews, threads, and blockers | [PR status, check mode](../playbooks/pr/babysit.md) |
| Perform a maintainer-quality review | [PR review](../workflows/pr/review/workflow.md) |
| Explicitly challenge a diff with fresh views (`interrogate`) | [Adversarial review method](../workflows/pr/review/methods/interrogate.md) |
| Apply a confirmed focused PR fix | [PR fix](../workflows/pr/fix/workflow.md) |
| Rebase or sync the PR branch | [Rebase](../workflows/pr/rebase/workflow.md) |
| Inspect or change labels | [Labels](../workflows/pr/labels/workflow.md) |
| Inspect or update title/body | [Metadata](../workflows/pr/metadata/workflow.md) |
| Prepare, reuse, inspect, or safely clean a branch worktree | [Worktree lifecycle](../workflows/pr/worktree/workflow.md) |
| Inventory worktrees, then perform only authorized cleanup | [Worktree cleanup](../playbooks/pr/worktree-cleanup.md) |
| Open a PR when requested | [Opening a PR](../playbooks/pr/opening-a-pr.md) |
| Land or release explicitly authorized changes | [Shipping](../playbooks/pr/shipping.md) |

PR review owns snapshot selection, actionable findings, and exact review-event authorization. The adversarial method is supplemental, not a replacement or a reason to publish. Use the worktree helper for lifecycle operations; the shared helper's inventory command is read-only. For multiple independent PRs or a stack, load the [coordinate route](coordinate.md) only when that broader task was requested.

Do not activate `nanobot-gate` from this route. Its literal user invocation is required even for readiness or shipping work.
