---
name: pr-worktree
description: Use when any GitHub PR workflow needs to checkout, inspect, review, test, or modify a PR locally without disturbing the current workspace; drive isolated review/fix worktree preparation, status checks, and safe cleanup through the bundled deterministic helper
---

# PR Worktree

Use the bundled script as the source of truth. It resolves PR metadata, selects the base remote, fetches current base/PR refs, chooses an ignored or sibling path, creates or safely reuses the worktree, and returns a machine-readable manifest. Do not make the LLM reconstruct that lifecycle with ad hoc shell commands.

## Non-negotiables

- Never run `gh pr checkout` or switch branches in the user's current workspace.
- Use `review` mode for read/test/review work and `fix` mode only when the user authorized commits and pushes.
- Refuse to reuse a dirty, foreign, or unregistered path. Do not stash, reset, clean, or overwrite it.
- Review mode must be detached at the fetched PR head. Fix mode must be attached to the PR head branch with upstream information.
- Run all subsequent commands with `workdir` set to the manifest's worktree path.
- Keep worktrees after triage/review for follow-up. Clean up only when the user asks.
- Never force-push or force-remove through this skill.

## Prepare

From any path inside the base repository:

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
- branch/detached/upstream/clean state;
- the checked-out head's relation to PR metadata (`match`, local ahead, behind, or diverged);
- ready-to-run diff/status/push commands.

In review mode, the helper refuses a stale, behind, or diverged checkout. In fix mode it preserves a branch that is locally ahead of GitHub metadata, but refuses behind or diverged state so existing maintainer commits are never reset implicitly. For cross-repository fixes, treat `maintainerCanModify: false` as a warning that the eventual push may be rejected; do not change remotes or invent a replacement branch without user direction.

## Work from the manifest

Set the tool `workdir` to the returned path. Use the returned base tracking ref for the three-dot diff. Do not fetch or rediscover metadata again unless the PR head changes while the task is active.

Before edits in fix mode, confirm:

```bash
git branch --show-current
git status --short --branch
git remote -v
```

The branch must be attached and the worktree clean.

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

Cleanup refuses dirty worktrees, attached branches without upstreams, and branches with unpushed commits. Report the refusal; do not bypass it with `--force` or manual deletion.

## Failure handling

- **Dirty/reused path**: preserve it and report the status preview.
- **Foreign/unregistered path**: choose a new explicit path or ask the user; never delete it.
- **PR ref fetch fails**: verify repository/remote/permissions, then report the exact command error.
- **Fix checkout is detached or branch is already checked out elsewhere**: stop; do not force checkout.
- **Contributor fork is unwritable**: report that direct maintainer push is unavailable and request direction.
- **Helper unavailable**: only then use a manual worktree fallback, preserving every non-negotiable above.
