#!/usr/bin/env python3
"""Prepare, inspect, and safely remove isolated GitHub PR worktrees."""

from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any

PR_FIELDS = (
    "number,title,state,isDraft,url,baseRefName,headRefName,headRefOid,"
    "headRepository,headRepositoryOwner,isCrossRepository,maintainerCanModify"
)


class CommandError(RuntimeError):
    def __init__(self, args: list[str], cwd: Path | None, stderr: str) -> None:
        self.args_list = args
        self.cwd = cwd
        self.stderr = stderr.strip()
        where = f" (cwd={cwd})" if cwd is not None else ""
        super().__init__(f"command failed{where}: {display_command(args)}\n{self.stderr}")


def run(
    args: list[str],
    *,
    cwd: Path | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        args,
        cwd=cwd,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and proc.returncode != 0:
        raise CommandError(args, cwd, proc.stderr)
    return proc


def output(args: list[str], *, cwd: Path | None = None) -> str:
    return run(args, cwd=cwd).stdout.strip()


def display_command(args: list[str]) -> str:
    return shlex.join(args)


def repo_root(repo_dir: str) -> Path:
    start = Path(repo_dir).expanduser().resolve()
    return Path(output(["git", "rev-parse", "--show-toplevel"], cwd=start)).resolve()


def git_common_dir(worktree: Path) -> Path:
    raw = output(["git", "rev-parse", "--git-common-dir"], cwd=worktree)
    path = Path(raw)
    if not path.is_absolute():
        path = worktree / path
    return path.resolve()


def parse_repo_from_pr_url(url: str) -> str:
    match = re.match(r"https?://[^/]+/([^/]+/[^/]+)/pull/\d+(?:/.*)?$", url)
    if not match:
        raise RuntimeError(f"cannot determine base repository from PR URL: {url}")
    return match.group(1)


def remote_repo_slug(url: str) -> str | None:
    text = url.strip().rstrip("/")
    if text.endswith(".git"):
        text = text[:-4]
    scp = re.match(r"^[^@]+@[^:]+:(.+/.+)$", text)
    if scp:
        text = scp.group(1)
    else:
        match = re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://[^/]+/(.+/.+)$", text)
        if match:
            text = match.group(1)
    parts = [part for part in text.replace("\\", "/").split("/") if part]
    if len(parts) < 2:
        return None
    return "/".join(parts[-2:]).lower()


def pr_metadata(pr: str, repo: str | None, root: Path) -> dict[str, Any]:
    args = ["gh", "pr", "view", pr, "--json", PR_FIELDS]
    if repo:
        args.extend(["--repo", repo])
    data = json.loads(output(args, cwd=root))
    data["baseRepository"] = parse_repo_from_pr_url(str(data["url"]))
    head_repo = data.get("headRepository") or {}
    if isinstance(head_repo, dict):
        name_with_owner = head_repo.get("nameWithOwner")
        if not name_with_owner and head_repo.get("name"):
            owner = (data.get("headRepositoryOwner") or {}).get("login")
            name_with_owner = f"{owner}/{head_repo['name']}" if owner else head_repo["name"]
        data["headRepositoryNameWithOwner"] = name_with_owner
    return data


def select_remote(root: Path, base_repo: str, requested: str | None) -> str:
    remotes = [line for line in output(["git", "remote"], cwd=root).splitlines() if line]
    if not remotes:
        raise RuntimeError("repository has no git remotes")
    if requested:
        if requested not in remotes:
            raise RuntimeError(f"remote {requested!r} does not exist; available: {', '.join(remotes)}")
        return requested

    target = base_repo.lower()
    for remote in remotes:
        url = output(["git", "remote", "get-url", remote], cwd=root)
        if remote_repo_slug(url) == target:
            return remote
    if "origin" in remotes:
        return "origin"
    return remotes[0]


def is_ignored(root: Path, path: Path) -> bool:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return False
    proc = run(["git", "check-ignore", "-q", "--", str(relative)], cwd=root, check=False)
    return proc.returncode == 0


def default_worktree_path(root: Path, number: int, mode: str) -> Path:
    local_root = root / ".worktrees"
    suffix = f"pr-{number}" if mode == "review" else f"pr-{number}-fix"
    if local_root.is_dir() or is_ignored(root, local_root):
        return (local_root / suffix).resolve()
    sibling = f"{root.name}-pr-{number}" if mode == "review" else f"{root.name}-pr-{number}-fix"
    return (root.parent / sibling).resolve()


def resolve_worktree_path(root: Path, raw: str | None, number: int, mode: str) -> Path:
    if not raw:
        return default_worktree_path(root, number, mode)
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = root / path
    return path.resolve()


def status_lines(path: Path, *, include_untracked: bool = False) -> list[str]:
    untracked = "normal" if include_untracked else "no"
    raw = output(
        ["git", "status", "--porcelain", f"--untracked-files={untracked}"],
        cwd=path,
    )
    return raw.splitlines() if raw else []


def untracked_status_lines(path: Path) -> list[str]:
    return [line for line in status_lines(path, include_untracked=True) if line.startswith("?? ")]


def ensure_reusable_worktree(root: Path, path: Path) -> None:
    if not path.exists():
        return
    if not path.is_dir():
        raise RuntimeError(f"worktree path exists but is not a directory: {path}")
    try:
        same_repo = git_common_dir(root) == git_common_dir(path)
    except (CommandError, RuntimeError) as exc:
        raise RuntimeError(f"existing path is not a registered worktree: {path}") from exc
    if not same_repo:
        raise RuntimeError(f"existing worktree belongs to another repository: {path}")
    dirty = status_lines(path)
    if dirty:
        preview = "\n".join(dirty[:20])
        raise RuntimeError(f"refusing to reuse dirty worktree {path}:\n{preview}")


def fetch_refs(root: Path, remote: str, metadata: dict[str, Any]) -> tuple[str, str]:
    number = int(metadata["number"])
    base = str(metadata["baseRefName"])
    base_ref = f"refs/remotes/{remote}/{base}"
    pr_ref = f"refs/remotes/{remote}/pr/{number}"
    output(
        ["git", "fetch", remote, f"+refs/heads/{base}:{base_ref}"],
        cwd=root,
    )
    output(
        ["git", "fetch", remote, f"+refs/pull/{number}/head:{pr_ref}"],
        cwd=root,
    )
    return base_ref, pr_ref


def prepare_review_worktree(root: Path, path: Path, pr_ref: str) -> None:
    if path.exists():
        output(["git", "checkout", "--detach", pr_ref], cwd=path)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    output(["git", "worktree", "add", "--detach", str(path), pr_ref], cwd=root)


def prepare_fix_worktree(
    root: Path,
    path: Path,
    base_ref: str,
    pr: str,
    base_repo: str,
) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        output(["git", "worktree", "add", "--detach", str(path), base_ref], cwd=root)
    args = ["gh", "pr", "checkout", pr, "--repo", base_repo]
    output(args, cwd=path)


def upstream(path: Path) -> str | None:
    proc = run(
        ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"],
        cwd=path,
        check=False,
    )
    return proc.stdout.strip() if proc.returncode == 0 else None


def worktree_status(path: Path) -> dict[str, Any]:
    branch = output(["git", "branch", "--show-current"], cwd=path)
    dirty = status_lines(path)
    untracked = untracked_status_lines(path)
    return {
        "path": str(path),
        "headOid": output(["git", "rev-parse", "HEAD"], cwd=path),
        "branch": branch or None,
        "detached": not bool(branch),
        "upstream": upstream(path),
        "clean": not dirty,
        "status": dirty,
        "untracked": untracked,
    }


def commit_is_ancestor(path: Path, older: str, newer: str) -> bool:
    proc = run(
        ["git", "merge-base", "--is-ancestor", older, newer],
        cwd=path,
        check=False,
    )
    if proc.returncode == 0:
        return True
    if proc.returncode == 1:
        return False
    detail = proc.stderr.strip() or proc.stdout.strip() or f"exit {proc.returncode}"
    raise RuntimeError(f"cannot compare PR head commits {older} and {newer}: {detail}")


def head_relation(path: Path, expected: str, actual: str) -> str:
    if not expected:
        return "metadata-unavailable"
    if expected == actual:
        return "match"
    if commit_is_ancestor(path, expected, actual):
        return "local-ahead-of-metadata"
    if commit_is_ancestor(path, actual, expected):
        return "behind-metadata"
    return "diverged-from-metadata"


def prepare(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(args.repo_dir)
    metadata = pr_metadata(args.pr, args.repo, root)
    remote = select_remote(root, str(metadata["baseRepository"]), args.remote)
    path = resolve_worktree_path(root, args.path, int(metadata["number"]), args.mode)
    if path == root:
        raise RuntimeError("refusing to use the base repository worktree as a PR worktree")
    ensure_reusable_worktree(root, path)
    if path.exists():
        existing = worktree_status(path)
        if args.mode == "review" and existing["branch"]:
            raise RuntimeError(
                f"refusing to detach an existing attached worktree branch: {existing['branch']}"
            )
        if (
            args.mode == "fix"
            and existing["branch"]
            and existing["branch"] != metadata.get("headRefName")
        ):
            raise RuntimeError(
                "refusing to switch an existing worktree from unrelated branch "
                f"{existing['branch']} to {metadata.get('headRefName')}"
            )
    base_ref, pr_ref = fetch_refs(root, remote, metadata)

    if args.mode == "review":
        prepare_review_worktree(root, path, pr_ref)
    else:
        prepare_fix_worktree(root, path, base_ref, args.pr, str(metadata["baseRepository"]))

    state = worktree_status(path)
    if not state["clean"]:
        raise RuntimeError(f"prepared worktree unexpectedly became dirty: {path}")
    if args.mode == "review" and not state["detached"]:
        raise RuntimeError(f"review worktree must be detached, found branch {state['branch']}")
    if args.mode == "fix" and state["detached"]:
        raise RuntimeError("fix worktree is detached; gh did not attach the PR head branch")

    expected_head = str(metadata.get("headRefOid") or "")
    relation = head_relation(path, expected_head, str(state["headOid"]))
    if args.mode == "review" and relation not in {"match", "metadata-unavailable"}:
        raise RuntimeError(
            f"review checkout is stale ({relation}); rerun prepare to fetch the current PR head"
        )
    if args.mode == "fix" and relation in {"behind-metadata", "diverged-from-metadata"}:
        raise RuntimeError(
            f"fix checkout is unsafe ({relation}); inspect the branch without resetting it"
        )
    result = {
        "action": "prepared",
        "mode": args.mode,
        "repoRoot": str(root),
        "baseRepository": metadata["baseRepository"],
        "headRepository": metadata.get("headRepositoryNameWithOwner"),
        "pr": metadata["number"],
        "title": metadata.get("title"),
        "url": metadata.get("url"),
        "state": metadata.get("state"),
        "isDraft": metadata.get("isDraft"),
        "isCrossRepository": metadata.get("isCrossRepository"),
        "maintainerCanModify": metadata.get("maintainerCanModify"),
        "baseRefName": metadata.get("baseRefName"),
        "headRefName": metadata.get("headRefName"),
        "expectedHeadOid": expected_head,
        "headMatchesMetadata": relation in {"match", "metadata-unavailable"},
        "headRelation": relation,
        "remote": remote,
        "baseTrackingRef": base_ref,
        "prTrackingRef": pr_ref,
        "worktree": state,
        "next": {
            "diff": ["git", "diff", f"{base_ref}...HEAD"],
            "status": ["git", "status", "--short", "--branch"],
        },
    }
    if args.mode == "fix":
        result["next"]["push"] = ["git", "push"]
    return result


def ahead_of_upstream(path: Path, upstream_ref: str) -> int:
    raw = output(["git", "rev-list", "--left-right", "--count", f"{upstream_ref}...HEAD"], cwd=path)
    parts = raw.split()
    if len(parts) != 2:
        raise RuntimeError(f"unexpected rev-list output: {raw}")
    return int(parts[1])


def cleanup(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(args.repo_dir)
    path = Path(args.path).expanduser()
    if not path.is_absolute():
        path = root / path
    path = path.resolve()
    if path == root:
        raise RuntimeError("refusing to remove the base repository worktree")
    ensure_reusable_worktree(root, path)
    if not path.exists():
        return {"action": "not-found", "path": str(path)}

    state = worktree_status(path)
    if not state["clean"]:
        raise RuntimeError(f"refusing to remove dirty worktree: {path}")
    if state["untracked"]:
        preview = "\n".join(state["untracked"][:20])
        raise RuntimeError(f"refusing to remove worktree with untracked files {path}:\n{preview}")
    if state["branch"]:
        if not state["upstream"]:
            raise RuntimeError(f"refusing to remove attached branch without upstream: {state['branch']}")
        ahead = ahead_of_upstream(path, str(state["upstream"]))
        if ahead:
            raise RuntimeError(f"refusing to remove worktree with {ahead} unpushed commit(s): {path}")

    output(["git", "worktree", "remove", str(path)], cwd=root)
    output(["git", "worktree", "prune"], cwd=root)
    return {"action": "removed", "path": str(path)}


def inspect_status(args: argparse.Namespace) -> dict[str, Any]:
    path = Path(args.path).expanduser().resolve()
    if not path.is_dir():
        raise RuntimeError(f"worktree does not exist: {path}")
    return {"action": "status", "worktree": worktree_status(path)}


def render_markdown(result: dict[str, Any]) -> str:
    action = result["action"]
    if action == "prepared":
        worktree = result["worktree"]
        lines = [
            f"# PR worktree: {result['mode']}",
            f"- PR: {result['baseRepository']}#{result['pr']} — {result.get('title')}",
            f"- URL: {result.get('url')}",
            f"- Path: `{worktree['path']}`",
            f"- Base: `{result['baseTrackingRef']}`",
            f"- Head: `{worktree['headOid']}` (relation: {result['headRelation']})",
            f"- Branch: `{worktree.get('branch') or '(detached)'}`",
            f"- Upstream: `{worktree.get('upstream') or '(none)'}`",
            f"- Clean: {worktree['clean']}",
            f"- Untracked entries: {len(worktree['untracked'])}",
            f"- Cross-repository: {result.get('isCrossRepository')}; maintainer can modify: {result.get('maintainerCanModify')}",
            "\n## Next commands",
        ]
        for name, command in result["next"].items():
            lines.append(f"- {name}: `{display_command(command)}` (cwd: `{worktree['path']}`)")
        return "\n".join(lines)
    if action == "status":
        worktree = result["worktree"]
        return "\n".join(
            [
                "# PR worktree status",
                f"- Path: `{worktree['path']}`",
                f"- Head: `{worktree['headOid']}`",
                f"- Branch: `{worktree.get('branch') or '(detached)'}`",
                f"- Upstream: `{worktree.get('upstream') or '(none)'}`",
                f"- Clean: {worktree['clean']}",
                *(f"- Change: `{line}`" for line in worktree["status"]),
                *(f"- Untracked: `{line[3:]}`" for line in worktree["untracked"]),
            ]
        )
    return f"# PR worktree cleanup\n- Action: {action}\n- Path: `{result['path']}`"


def emit(result: dict[str, Any], format_name: str) -> None:
    if format_name == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(result))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare_parser = subparsers.add_parser("prepare", help="create or safely reuse a PR worktree")
    prepare_parser.add_argument("pr", help="PR number or URL accepted by gh")
    prepare_parser.add_argument("--repo", help="base OWNER/REPO when not implied by the current gh context")
    prepare_parser.add_argument("--repo-dir", default=".", help="path inside the base repository")
    prepare_parser.add_argument("--mode", choices=("review", "fix"), default="review")
    prepare_parser.add_argument("--path", help="explicit worktree path; relative paths resolve from repo root")
    prepare_parser.add_argument("--remote", help="base repository remote; auto-detected by URL by default")
    prepare_parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    prepare_parser.set_defaults(handler=prepare)

    status_parser = subparsers.add_parser("status", help="report a prepared worktree's safety state")
    status_parser.add_argument("--path", required=True, help="worktree path")
    status_parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    status_parser.set_defaults(handler=inspect_status)

    cleanup_parser = subparsers.add_parser("cleanup", help="remove a clean worktree with no unpushed commits")
    cleanup_parser.add_argument("--path", required=True, help="worktree path")
    cleanup_parser.add_argument("--repo-dir", default=".", help="path inside the base repository")
    cleanup_parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    cleanup_parser.set_defaults(handler=cleanup)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        result = args.handler(args)
    except (CommandError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    emit(result, args.format)


if __name__ == "__main__":
    main()
