# Linear Issue–PR relationships

Load only when preparing or updating an authorized PR associated with a known Linear Issue. Skip when no such task is involved; do not require a connector installation. Link semantics are not permission to publish, merge, change integration settings, or close/reopen an Issue outside the agreed task scope.

## Choose the relationship per Issue

| Relationship | Use when | Canonical PR description line | Structured type, if exposed |
|---|---|---|---|
| Resolves | Delivery through this PR to its intended target completes the full agreed Issue scope, with no remaining implementation or acceptance work that must keep it open | `Resolves TEAM-123` | `closes` |
| Contributes | The PR implements part of the task, an intermediate step, or work with remaining acceptance/delivery requirements | `Contributes to TEAM-123` | `contributes` |
| Related | The Issue supplies context or a related concern, but this PR does not deliver its implementation | `Related to TEAM-123` | `links` |

`TEAM-123` is an example, not a destination. Use real confirmed Issue identifiers and the capabilities/names in the actual connector schema. `Fixes` and `Closes` have the same closing intent as `Resolves`; do not use them casually to mean “related”.

Closing links participate in the team's configured PR workflow, including the merge transition. Contributing links may advance earlier workflow stages but do not apply the merge transition. Related links are reference-only and do not automate Issue status. `Refs`/`References` are contributing magic words, not reference-only links; prefer the unambiguous canonical lines above.

## Establish an effective link

1. Check the current Issue agreement and actual PR scope before choosing the type. For several Issues, choose separately: one PR can resolve one Issue, contribute to another, and only relate to a third. Do not bundle them all under a closing keyword.
2. Within authorized PR metadata editing, put the chosen magic-word line in the PR description, or use an exposed structured Issue–PR linking action. Do not assume a pasted URL, an Issue Resources attachment, or a PR comment establishes the intended typed relationship. Magic words in PR comments do not create these links.
3. Keep existing correct relationships. Reconcile task-owned stale or contradictory links within the authorized metadata scope; do not blindly preserve a closing keyword after scope narrows. Check title/body and visible auto-links: an Issue ID in a branch or title can create an association without expressing the intended partial/reference-only semantics. Do not rename branches, rewrite commits, or unlink unrelated work to work around this.
4. Read back the published PR metadata and, when accessible, the native Issue–PR association and its type. Distinguish “description marker verified” from “native association verified”. If access, integration, or synchronization prevents verification, state that limit instead of claiming the workflow is connected. Do not repeatedly add duplicate attachments or comments.

## Multiple PRs and merge behavior

- For incremental or stacked work, use Contributes for partial/intermediate delivery. A PR merged only into another feature branch is not evidence of final integration into the Issue's agreed target.
- When the final delivery PR covers the complete Issue, link it explicitly with Resolves. Links from earlier PRs are not automatically inherited by a later integration PR. Consider remaining linked work and acceptance requirements before promoting any relationship to closing.
- Automatic status changes require the relevant repository's Linear–GitHub integration and the team's workflow rules. The target branch can map to a review/QA/deployment state or no action, not necessarily Done. Do not change these settings or promise automatic closure merely because a magic word exists.
- During an authorized post-merge check, verify actual target integration, full acceptance coverage, the effective relationship, and the observed Issue status. If automation is absent or disagrees with the agreed completion condition, report the mismatch; perform a manual transition only within task authority. Do not start continuous monitoring or mark Done at PR creation.

Source: [Linear GitHub integration documentation](https://linear.app/docs/github#magic-words), including linking multiple Issues/PRs and target-branch workflow rules.
