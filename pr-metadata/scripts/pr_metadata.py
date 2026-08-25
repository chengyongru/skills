#!/usr/bin/env python3
"""Inspect, plan, and verify GitHub pull-request title/body updates."""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

PR_URL_RE = re.compile(
    r"^https?://github\.com/([^/]+)/([^/]+)/pull/(\d+)(?:[/?#].*)?$",
    re.IGNORECASE,
)


class CommandError(RuntimeError):
    def __init__(
        self, args: list[str], returncode: int, stdout: str, stderr: str
    ) -> None:
        detail = stderr.strip() or stdout.strip() or f"exit {returncode}"
        super().__init__(f"command failed ({returncode}): {' '.join(args)}\n{detail}")


def run(
    args: list[str],
    *,
    cwd: Path | None = None,
    input_text: str | None = None,
) -> str:
    env = dict(os.environ)
    env.setdefault("NO_COLOR", "1")
    try:
        proc = subprocess.run(
            args,
            cwd=cwd,
            env=env,
            input=input_text,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        raise RuntimeError(f"cannot run {args[0]}: {exc}") from exc
    if proc.returncode != 0:
        raise CommandError(args, proc.returncode, proc.stdout, proc.stderr)
    return proc.stdout


def api_json(
    endpoint: str,
    *,
    method: str = "GET",
    body: dict[str, Any] | None = None,
) -> Any:
    args = ["gh", "api", endpoint]
    if method != "GET":
        args.extend(["-X", method])
    input_text = None
    if body is not None:
        args.extend(["--input", "-"])
        input_text = json.dumps(body, ensure_ascii=False)
    raw = run(args, input_text=input_text)
    return json.loads(raw) if raw.strip() else None


def normalize_repo(value: str) -> str:
    parts = value.strip().strip("/").split("/")
    if len(parts) != 2 or not all(parts):
        raise RuntimeError("repository must be OWNER/REPO")
    return f"{parts[0]}/{parts[1]}"


def resolve_target(
    pr_value: str,
    repo_value: str | None,
    repo_dir: str | None,
) -> tuple[str, int]:
    match = PR_URL_RE.match(pr_value.strip())
    url_repo: str | None = None
    if match:
        url_repo = f"{match.group(1)}/{match.group(2)}"
        number = int(match.group(3))
    else:
        try:
            number = int(pr_value)
        except ValueError as exc:
            raise RuntimeError(
                "PR must be a positive number or GitHub pull-request URL"
            ) from exc
    if number <= 0:
        raise RuntimeError("PR number must be positive")

    explicit_repo = normalize_repo(repo_value) if repo_value else None
    if explicit_repo and url_repo and explicit_repo.casefold() != url_repo.casefold():
        raise RuntimeError(
            f"--repo {explicit_repo} conflicts with PR URL repository {url_repo}"
        )
    repo = explicit_repo or url_repo
    if not repo:
        cwd = Path(repo_dir).expanduser().resolve() if repo_dir else None
        repo = run(
            [
                "gh",
                "repo",
                "view",
                "--json",
                "nameWithOwner",
                "--jq",
                ".nameWithOwner",
            ],
            cwd=cwd,
        ).strip()
        repo = normalize_repo(repo)
    return repo, number


def inspect_pr(repo: str, pr: int) -> dict[str, Any]:
    pull = api_json(f"repos/{repo}/pulls/{pr}")
    return {
        "repo": repo,
        "pr": pr,
        "url": pull.get("html_url"),
        "title": str(pull.get("title") or ""),
        "body": str(pull.get("body") or ""),
    }


def proposed_body(args: argparse.Namespace) -> str | None:
    if args.body is not None and args.body_file is not None:
        raise RuntimeError("use only one of --body and --body-file")
    if args.body_file is None:
        return args.body
    path = Path(args.body_file).expanduser().resolve()
    if not path.is_file():
        raise RuntimeError(f"body file does not exist: {path}")
    return path.read_text(encoding="utf-8")


def plan_update(
    before: dict[str, Any],
    title: str | None,
    body: str | None,
) -> dict[str, Any]:
    if title is None and body is None:
        raise RuntimeError("update requires --title, --body, or --body-file")
    if title is not None and not title.strip():
        raise RuntimeError("PR title must not be blank")
    proposed = {
        "title": before["title"] if title is None else title,
        "body": before["body"] if body is None else body,
    }
    changed = [field for field in ("title", "body") if proposed[field] != before[field]]
    return {"proposed": proposed, "changedFields": changed, "changed": bool(changed)}


def verify_after(after: dict[str, Any], plan: dict[str, Any]) -> None:
    mismatches = {
        field: {"expected": plan["proposed"][field], "actual": after[field]}
        for field in plan["changedFields"]
        if after[field] != plan["proposed"][field]
    }
    if mismatches:
        raise RuntimeError(
            "PR metadata verification failed: "
            + json.dumps(mismatches, ensure_ascii=False)
        )


def inspect_command(args: argparse.Namespace) -> dict[str, Any]:
    repo, pr = resolve_target(args.pr, args.repo, args.repo_dir)
    return {"action": "inspected", **inspect_pr(repo, pr)}


def update_command(args: argparse.Namespace) -> dict[str, Any]:
    repo, pr = resolve_target(args.pr, args.repo, args.repo_dir)
    body = proposed_body(args)
    if args.simulate_current_json is not None:
        if args.apply:
            raise RuntimeError("simulation cannot be used with --apply")
        before = json.loads(args.simulate_current_json)
        if not isinstance(before, dict) or not all(
            isinstance(before.get(field), str) for field in ("title", "body")
        ):
            raise RuntimeError(
                "--simulate-current-json requires string title and body fields"
            )
        before = {"repo": repo, "pr": pr, "url": None, **before}
    else:
        before = inspect_pr(repo, pr)

    plan = plan_update(before, args.title, body)
    if args.apply and plan["changed"]:
        payload = {field: plan["proposed"][field] for field in plan["changedFields"]}
        api_json(f"repos/{repo}/pulls/{pr}", method="PATCH", body=payload)
        after = inspect_pr(repo, pr)
        verify_after(after, plan)
        action = "updated"
    elif args.apply:
        after = before
        action = "no-op"
    else:
        after = None
        action = "planned"
    return {
        "action": action,
        "repo": repo,
        "pr": pr,
        "url": before.get("url"),
        "dryRun": not args.apply,
        "mutationPerformed": action == "updated",
        "before": {"title": before["title"], "body": before["body"]},
        **plan,
        "after": (
            {"title": after["title"], "body": after["body"]}
            if after is not None
            else None
        ),
    }


def body_diff(before: str, after: str) -> list[str]:
    return list(
        difflib.unified_diff(
            before.splitlines(),
            after.splitlines(),
            fromfile="before/body",
            tofile="after/body",
            lineterm="",
        )
    )


def render_markdown(result: dict[str, Any]) -> str:
    if result["action"] == "inspected":
        return "\n".join(
            [
                "# PR metadata",
                f"- PR: {result['repo']}#{result['pr']}",
                f"- URL: {result.get('url')}",
                f"- Title: {result['title']}",
                "\n## Description",
                result["body"] or "(empty)",
            ]
        )

    before = result["before"]
    proposed = result["proposed"]
    lines = [
        f"# PR metadata: {result['action']}",
        f"- PR: {result['repo']}#{result['pr']}",
        f"- Changed fields: {', '.join(result['changedFields']) or '(none)'}",
        f"- Title before: {before['title']}",
        f"- Title proposed: {proposed['title']}",
    ]
    if "body" in result["changedFields"]:
        lines.extend(["\n## Description diff", "```diff"])
        lines.extend(body_diff(before["body"], proposed["body"]))
        lines.append("```")
    lines.append(
        "- GitHub mutation: verified"
        if result["mutationPerformed"]
        else "- GitHub mutation: not performed"
    )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect and safely update GitHub PR title/description."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect = subparsers.add_parser("inspect", help="Read PR title and description")
    inspect.add_argument("pr", help="PR number or GitHub PR URL")
    inspect.add_argument("--repo", help="OWNER/REPO; inferred from URL or cwd")
    inspect.add_argument("--repo-dir", help="Repository path used to infer --repo")
    inspect.add_argument("--format", choices=("json", "markdown"), default="json")
    inspect.set_defaults(func=inspect_command)

    update = subparsers.add_parser(
        "update", help="Plan or apply title/body replacements"
    )
    update.add_argument("pr", help="PR number or GitHub PR URL")
    update.add_argument("--repo", help="OWNER/REPO; inferred from URL or cwd")
    update.add_argument("--repo-dir", help="Repository path used to infer --repo")
    update.add_argument("--title", help="Exact replacement title")
    update.add_argument("--body", help="Exact replacement description")
    update.add_argument(
        "--body-file", help="UTF-8 file containing replacement description"
    )
    update.add_argument(
        "--apply", action="store_true", help="Perform and verify the update"
    )
    update.add_argument("--format", choices=("json", "markdown"), default="json")
    update.add_argument("--simulate-current-json", help=argparse.SUPPRESS)
    update.set_defaults(func=update_command)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        result = args.func(args)
    except (CommandError, RuntimeError, json.JSONDecodeError) as exc:
        parser.exit(2, f"error: {exc}\n")
    if args.format == "markdown":
        print(render_markdown(result))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
