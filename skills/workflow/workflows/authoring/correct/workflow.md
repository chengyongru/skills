# Correct

The operator keeps correcting agents in this repo for the same mistakes. Within the authorized scope, change the repo so the next agent cannot make them. A review-only request produces proposals, not edits. Use installed [pr-worktree](../../pr/worktree/workflow.md) for branch isolation and [repo-prose](../../writing/prose/workflow.md) for repository guidance when applicable.

Assume every contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. Design the repo so a change that looks right from one file is right for the whole repo.

## Find the mistake classes

First, read recent commits, reverts, review comments, agent instruction files, and comments that explain workarounds. Group the mistakes into classes. A class counts once it has happened twice.

## Fix each class at the highest level that works

1. **Eliminate it with architecture.** Give each piece of state one owner and each task one supported way. Hide internals so the wrong import fails. Replace hand-synced lists with one source of truth. Delete old ways and dead code an agent would copy.
2. **Enforce it with types so the bad state can't be written.** If bad code still compiles, add a lint or CI check whose error names the file, type, or function to use instead. If the pattern is already common, fail only when a change adds more.
3. **Test the behavior.** Fix or delete any test that still passes when the behavior it checks breaks, or that fails when only the internals change.
4. **Write docs or agent rules last, only for judgment calls.** Nothing fails when an agent skips them.

## Fix and prove

Fix the most frequent classes in separate verifiable units when editing is authorized. Prove each new check fails on a real past mistake in task-owned isolation; never reset or overwrite another contributor's work to recreate it. Run the same check locally as the repository uses in CI, without publishing or triggering a remote run implicitly. Exceptions go on the offending line with a reason, an expiry date, and a human's approval. Commit or publish only when separately authorized.

## Keep the rule table

When authorized to edit project guidance, keep a table pairing each rule with its enforcement. A correction is evidence to inspect, not automatic permission to persist a new rule. If an existing rule has no enforcement and the mistake recurs, fix it at the highest level within scope; drop the redundant rule once the mistake cannot happen.

Do not edit `SOUL.md`, `USER.md`, `memory/MEMORY.md`, the protected history journal, or root configuration. Packaged guidance stays immutable: propose a patch outside the plugin unless a plugin change was expressly requested, then require review and re-enabling after it is final. Standalone skill changes require an authorized `<agent-workspace>/skills/<name>/SKILL.md` target and installed `skill-creator` when available.

**Reply:** each class with its evidence, the level you picked, and why a higher level didn't work.
