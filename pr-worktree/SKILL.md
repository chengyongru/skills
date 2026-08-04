---
name: pr-worktree
description: Use when any GitHub PR workflow needs an isolated worktree, including starting a new PR from a base branch, resuming a local branch before a PR exists, inspecting/reviewing an existing PR, testing it, or making authorized maintainer fixes; drive preparation, status checks, and safe cleanup through the bundled deterministic helper
---

# PR Worktree

Use the bundled script as the source of truth. It supports two lifecycles:

- `start`: create or safely reuse an attached local topic-branch worktree before a PR exists.
- `prepare`: resolve PR metadata, fetch current base/PR refs, and create or safely reuse a detached
  review worktree or an attached maintainer-fix worktree for an existing PR.

Both paths select a safe worktree location and return a machine-readable manifest. Do not make the LLM
reconstruct either lifecycle with ad hoc shell commands.

## Reuse before creating

Inspect the current worktree before invoking `start` or `prepare`. Reuse it directly when it is the
intended repository worktree and its branch/HEAD matches the task:

- For a new PR, reuse an existing non-base topic branch when its current changes are intentionally
  part of this task, even if the worktree is dirty.
- For an existing PR in `review` mode, reuse only a clean detached worktree at the PR head.
- For an existing PR in `fix` mode, reuse an attached worktree on that PR's head branch when its
  changes belong to the authorized fix.

When reusing, set every command's `workdir` to that path and do not create a second worktree merely
to obtain a manifest. Create or prepare a new worktree only when the current one is a base branch,
belongs to another task/PR, contains unrelated changes, or does not satisfy the requested mode.

## Choose the shortest path

- No PR exists yet: run `start <topic-branch>`, then use the manifest's `worktree.path` for all work.
- A PR number or URL exists: run `prepare <PR> --mode review` for review/tests, or `--mode fix` for
  explicitly authorized maintainer edits.
- Only need to inspect an already prepared worktree: run `status --path <worktree-path>`.

## Non-negotiables

- Never run `gh pr checkout` or switch branches in the user's current workspace.
- Use `start` before coding when a new PR does not exist yet, unless the current worktree already
  satisfies the reuse rules above. Use `prepare` only after a PR number or URL exists, unless the
  current worktree already satisfies the requested review/fix mode.
- Use `review` mode for read/test/review work and `fix` mode for authorized edits. Gate remediation
  is an explicit local-only exception: it may edit and verify, but does not commit or push until the
  gate passes.
- A `start` worktree is attached to a new local branch and is the only place where new changes should be made.
- Refuse to prepare/reuse a target path with tracked changes, or a foreign or unregistered path.
  Existing-PR `prepare` preserves untracked files without stashing, cleaning, or overwriting them.
  A `start` target must also be free of untracked files so a new branch never inherits an ambiguous
  directory. The direct-reuse exception for an already relevant in-progress topic worktree is defined
  above.
- Review mode must be detached at the fetched PR head. Fix mode must be attached to the PR head branch with upstream information.
- Run all subsequent commands with `workdir` set to the manifest's worktree path.
- Keep worktrees after triage/review for follow-up. Clean up only when the user asks.
- Never force-push or force-remove through this skill.

## Start a new PR from zero

First apply “Reuse before creating”. If the current worktree is already the intended topic branch,
continue there; do not run `start` just to create a duplicate path. Otherwise run this from any path
inside the base repository before editing:

```powershell
python <this-skill>\scripts\pr_worktree.py start codex/<short-topic> --repo <OWNER/REPO> --base main --format markdown
```

Use the returned `Path` as the `workdir` for all implementation, test, commit, and push commands. The
helper fetches the latest `<remote>/<base>` first and creates `codex/<short-topic>` from that commit.
It does not create a PR or push anything. After the work is committed, inspect remotes and explicitly
push to the user's fork, then create the PR:

```powershell
git push -u <fork-remote> codex/<short-topic>
gh pr create --repo <OWNER/REPO> --base main --head <fork-owner>:codex/<short-topic>
```

Once the PR exists, use the returned PR number with the existing `prepare` flow for the formal review.

The command is intentionally idempotent for a clean existing worktree on the same branch: it reports
`reused` rather than resetting, rebasing, or overwriting it. If the branch exists locally but has no
worktree, it safely attaches that branch without changing its commits. If the branch exists only on a
remote, choose a new branch or use the existing PR workflow; never silently fork it.

### Start edge cases

- A dirty current worktree is never changed. `start` creates the new worktree from the fetched base, so
  current uncommitted changes are **not copied**. The manifest warns about this. Commit or move those
  changes deliberately before using them in the new PR.
- `--source head` is available when a clean local `HEAD` (including its committed history) is the intended
  starting point. It refuses a dirty source because uncommitted changes cannot be copied safely.
- An existing target path must be a registered worktree of the same repository and must have no tracked
  or untracked changes. A foreign path, dirty path, detached path, or unrelated branch stops with an
  actionable error.
- An existing local branch is attached only if Git confirms it is not checked out elsewhere. An existing
  remote branch causes a stop rather than an accidental duplicate PR.
- If the base repository or remote cannot be inferred, pass `--repo OWNER/REPO` and, when necessary,
  `--remote <base-remote>` explicitly. The helper never invents a remote or pushes on the user's behalf.

## Prepare

For an existing PR, run from any path inside the base repository:

```bash
python3 <this-skill>/scripts/pr_worktree.py prepare <PR-number-or-URL> --repo <OWNER/REPO> --mode review --format markdown
```

For maintainer edits:

```bash
python3 <this-skill>/scripts/pr_worktree.py prepare <PR-number-or-URL> --repo <OWNER/REPO> --mode fix --format markdown
```

Omit `--repo` when the current GitHub repository context is unambiguous. Useful overrides:

- `--repo-dir <path>` when invoking outside the base repository root;
- `--path <path>` when an established worktree location is required;
- `--remote <name>` when remote URL auto-detection cannot select the base repository remote;
- `--format json` for orchestration.

Read the manifest once. It provides:

- PR/base/head repositories and refs;
- selected remote and worktree path;
- branch/detached/upstream/tracked-clean state and separately reported untracked entries;
- the checked-out head's relation to PR metadata (`match`, local ahead, behind, or diverged);
- ready-to-run diff/status/push commands.

For a new PR, the `start` manifest additionally provides the selected base tracking ref, source mode,
new branch, source-worktree warning, and the exact worktree path to use for subsequent commands.

In review mode, the helper refuses a stale, behind, or diverged checkout. In fix mode it preserves a branch that is locally ahead of GitHub metadata, but refuses behind or diverged state so existing maintainer commits are never reset implicitly. For cross-repository fixes, treat `maintainerCanModify: false` as a warning that the eventual push may be rejected; do not change remotes or invent a replacement branch without user direction.

## Work from the manifest

Set the tool `workdir` to the returned path. Use the returned base tracking ref for the three-dot diff. Do not fetch or rediscover metadata again unless the PR head changes while the task is active.

Before edits in fix mode, confirm:

```bash
git branch --show-current
git status --short --branch
git remote -v
```

The branch must be attached and tracked-clean. Untracked files may remain and must not be altered.

## Status

Use the helper instead of manually combining branch/head/dirty checks:

```bash
python3 <this-skill>/scripts/pr_worktree.py status --path <worktree-path> --format markdown
```

## Cleanup

Only when the user requests cleanup:

```bash
python3 <this-skill>/scripts/pr_worktree.py cleanup --repo-dir <base-repository> --path <worktree-path> --format markdown
```

Cleanup refuses tracked changes, untracked files, attached branches without upstreams, and branches with unpushed commits. Existing-PR prepare/reuse ignores untracked files, but cleanup preserves them rather than deleting them. Report the refusal; do not bypass it with `--force` or manual deletion.

## Failure handling

- **Tracked-dirty existing-PR path**: preserve it and report the status preview. Untracked-only paths
  are reusable for `prepare`; leave those files untouched.
- **Dirty or untracked new-PR target**: stop and choose a clean target path; never inherit, stash, or
  delete the files implicitly.
- **Reusable current worktree**: keep it and continue in place when the branch and intended change
  match the task; do not create a clean duplicate just because the current worktree has edits.
- **Foreign/unregistered path**: choose a new explicit path or ask the user; never delete it.
- **PR ref fetch fails**: verify repository/remote/permissions, then report the exact command error.
- **Fix checkout is detached or branch is already checked out elsewhere**: stop; do not force checkout.
- **Contributor fork is unwritable**: report that direct maintainer push is unavailable and request direction.
- **Helper unavailable**: only then use a manual worktree fallback, preserving every non-negotiable above.
- **Need to carry uncommitted changes into a new PR**: stop and make that transfer explicit. Do not use
  `start` expecting it to copy a dirty source worktree; first commit the intended changes in a deliberate
  branch or ask for a patch/snapshot workflow.
