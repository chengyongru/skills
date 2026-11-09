# Linear Issue–PR relationships

Load only when preparing or updating an authorized PR associated with a known Linear Issue. Skip when no such task is involved; do not require a connector installation. Link semantics are not permission to publish, merge, change integration settings, or close/reopen an Issue outside the agreed task scope.

## Choose the relationship per Issue

| Relationship | Use when | Canonical PR description line | Structured type, if exposed |
|---|---|---|---|
| Resolves | This PR is the intended final delivery: its changes, together with work already in the target, cover the full agreed Issue scope on merge, and the Issue can close then | `Resolves [TEAM-123](https://linear.app/WORKSPACE/issue/TEAM-123)` | `closes` |
| Contributes | The PR delivers only part of the scope, is an intermediate step, or the Issue must stay open after merge for remaining work or agreed acceptance | `Contributes to [TEAM-123](https://linear.app/WORKSPACE/issue/TEAM-123)` | `contributes` |
| Related | The Issue supplies context or a related concern, but this PR does not deliver its implementation | `Related to [TEAM-123](https://linear.app/WORKSPACE/issue/TEAM-123)` | `links` |

`TEAM-123` and `WORKSPACE` are placeholders, not destinations. Use the confirmed Issue identifier and URL, and the capabilities/names in the actual connector schema. `Fixes` and `Closes` have the same closing intent as `Resolves`; do not use them casually to mean “related”.

A closing relationship expresses the intended result of merging this PR, not a claim that the Issue is already done. Pending pre-merge CI, review, verification, or fixes intended for this same PR do not make an otherwise final delivery partial. Report unfinished checks and defects honestly and resolve them before merge as required. If the Issue must remain open for agreed post-merge acceptance, use Contributes until that condition can be met. If the actual scope or completion condition is unclear, clarify it rather than defaulting to Contributes.

Closing links participate in the team's configured PR workflow, including the merge transition. Contributing links may advance earlier workflow stages but do not apply the merge transition. Related links are reference-only and do not automate Issue status. `Refs`/`References` are contributing magic words, not reference-only links; prefer the unambiguous canonical lines above.

## Establish an effective link

1. Check the current Issue agreement, actual PR scope, and intended target before choosing the type. For several Issues, choose separately: one PR can resolve one Issue, contribute to another, and only relate to a third. Do not bundle them all under a closing keyword.
2. Within authorized PR metadata editing, put a magic-word line with a clickable Markdown Issue link in the PR description for each Issue this PR is deliberately associated with, even when using an exposed structured linking action. Obtain the URL from the Issue record or a confirmed task link; do not guess the workspace. If the URL is unavailable, ask for it or report the missing link when publishing an otherwise authorized PR with the correct magic word and identifier. A pasted URL, Issue Resources attachment, or PR comment alone does not establish the intended typed relationship; magic words in PR comments do not create these links.
3. Keep existing correct relationships. Reconcile task-owned stale or contradictory links within the authorized metadata scope; do not blindly preserve a closing keyword after scope narrows. Check title/body and visible auto-links: an Issue ID in a branch or title can create an association without expressing the intended partial/reference-only semantics. Do not rename branches, rewrite commits, or unlink unrelated work to work around this.
4. Read back the raw published PR body from the forge to check both the magic word and Markdown URL, and, when accessible, the native Issue–PR association and its type. A normalized Linear description alone does not prove the forge body contains a clickable link. Distinguish body verification from native association verification; if access, integration, or synchronization prevents verification, state that limit instead of claiming the workflow is connected. Do not repeatedly add duplicate attachments or comments.

## Multiple PRs and merge behavior

- For incremental or stacked work, use Contributes for partial/intermediate delivery. A PR merged only into another feature branch does not establish integration into a different agreed target.
- When the final delivery PR completes the Issue together with work already in its target, link it explicitly with Resolves. Its own incremental diff need not repeat those earlier changes. Links from earlier PRs are not automatically inherited by a later integration PR. Consider remaining work and the agreed completion condition before choosing a closing relationship.
- Automatic status changes require the relevant repository's Linear–GitHub integration and the team's workflow rules. The target branch can map to a review/QA/deployment state or no action, not necessarily Done. Do not change these settings or promise automatic closure merely because a magic word exists.
- During an authorized post-merge check, verify actual target integration, full acceptance coverage, the effective relationship, and the observed Issue status. If automation is absent or disagrees with the agreed completion condition, report the mismatch; perform a manual transition only within task authority. Do not start continuous monitoring or mark Done at PR creation.

Source: [Linear GitHub integration documentation](https://linear.app/docs/github#magic-words), including linking multiple Issues/PRs and target-branch workflow rules.
