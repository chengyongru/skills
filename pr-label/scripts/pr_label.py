#!/usr/bin/env python3
"""Inspect and safely update existing labels on a GitHub pull request."""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any
from urllib.parse import quote

PR_URL_RE = re.compile(r"^https?://github\.com/([^/]+)/([^/]+)/pull/(\d+)(?:[/?#].*)?$", re.IGNORECASE)


class CommandError(RuntimeError):
    def __init__(self, args: list[str], returncode: int, stdout: str, stderr: str) -> None:
        self.args_list = args
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        detail = stderr.strip() or stdout.strip() or f"exit {returncode}"
        super().__init__(f"command failed ({returncode}): {' '.join(args)}\n{detail}")


def run(
    args: list[str],
    *,
    cwd: Path | None = None,
    body: dict[str, Any] | None = None,
) -> str:
    env = dict(os.environ)
    env.setdefault("NO_COLOR", "1")
    tmp_path: Path | None = None
    command = list(args)
    try:
        if body is not None:
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as tmp:
                json.dump(body, tmp, ensure_ascii=False)
                tmp_path = Path(tmp.name)
            command.extend(["--input", str(tmp_path)])
        try:
            proc = subprocess.run(
                command,
                cwd=cwd,
                env=env,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        except OSError as exc:
            raise RuntimeError(f"cannot run {command[0]}: {exc}") from exc
    finally:
        if tmp_path is not None:
            try:
                tmp_path.unlink()
            except FileNotFoundError:
                pass
    if proc.returncode != 0:
        raise CommandError(command, proc.returncode, proc.stdout, proc.stderr)
    return proc.stdout


def api_json(
    endpoint: str,
    *,
    method: str = "GET",
    body: dict[str, Any] | None = None,
    paginate: bool = False,
) -> Any:
    args = ["gh", "api", endpoint]
    if method != "GET":
        args.extend(["-X", method])
    if paginate:
        args.extend(["--paginate", "--slurp"])
    raw = run(args, body=body)
    return json.loads(raw) if raw.strip() else None


def normalize_repo(value: str) -> str:
    parts = value.strip().strip("/").split("/")
    if len(parts) != 2 or not all(parts):
        raise RuntimeError("repository must be OWNER/REPO")
    return f"{parts[0]}/{parts[1]}"


def resolve_target(pr_value: str, repo_value: str | None, repo_dir: str | None) -> tuple[str, int]:
    match = PR_URL_RE.match(pr_value.strip())
    url_repo: str | None = None
    if match:
        url_repo = f"{match.group(1)}/{match.group(2)}"
        number = int(match.group(3))
    else:
        try:
            number = int(pr_value)
        except ValueError as exc:
            raise RuntimeError("PR must be a positive number or GitHub pull-request URL") from exc
    if number <= 0:
        raise RuntimeError("PR number must be positive")

    explicit_repo = normalize_repo(repo_value) if repo_value else None
    if explicit_repo and url_repo and explicit_repo.casefold() != url_repo.casefold():
        raise RuntimeError(f"--repo {explicit_repo} conflicts with PR URL repository {url_repo}")
    repo = explicit_repo or url_repo
    if not repo:
        cwd = Path(repo_dir).expanduser().resolve() if repo_dir else None
        repo = run(
            ["gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"],
            cwd=cwd,
        ).strip()
        repo = normalize_repo(repo)
    return repo, number


def issue_labels(repo: str, pr: int) -> list[str]:
    payload = api_json(f"repos/{repo}/issues/{pr}")
    labels = payload.get("labels") or []
    return [str(item["name"]) for item in labels if isinstance(item, dict) and item.get("name")]


def repository_labels(repo: str) -> list[dict[str, Any]]:
    pages = api_json(f"repos/{repo}/labels?per_page=100", paginate=True) or []
    if pages and all(isinstance(item, dict) for item in pages):
        pages = [pages]
    labels: list[dict[str, Any]] = []
    for page in pages:
        if not isinstance(page, list):
            raise RuntimeError("unexpected repository-label response from GitHub")
        for item in page:
            if not isinstance(item, dict) or not item.get("name"):
                continue
            labels.append(
                {
                    "name": str(item["name"]),
                    "color": str(item.get("color") or ""),
                    "description": str(item.get("description") or ""),
                }
            )
    labels.sort(key=lambda item: item["name"].casefold())
    return labels


def inspect_pr(repo: str, pr: int) -> dict[str, Any]:
    pull = api_json(f"repos/{repo}/pulls/{pr}")
    return {
        "repo": repo,
        "pr": pr,
        "title": pull.get("title"),
        "url": pull.get("html_url"),
        "state": pull.get("state"),
        "draft": pull.get("draft"),
        "currentLabels": issue_labels(repo, pr),
        "availableLabels": repository_labels(repo),
    }


def label_key(value: str) -> str:
    return value.strip().casefold()


def dedupe(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        clean = value.strip()
        if not clean:
            raise RuntimeError("label names and exclusive prefixes must not be empty")
        key = label_key(clean)
        if key not in seen:
            seen.add(key)
            result.append(clean)
    return result


def canonical_additions(requested: list[str], available: list[str]) -> list[str]:
    by_key = {label_key(label): label for label in available}
    result: list[str] = []
    for value in dedupe(requested):
        key = label_key(value)
        if key not in by_key:
            suggestions = difflib.get_close_matches(value, available, n=3, cutoff=0.55)
            suffix = f"; nearby labels: {', '.join(suggestions)}" if suggestions else ""
            raise RuntimeError(f"target label does not exist in repository: {value}{suffix}")
        result.append(by_key[key])
    return result


def canonical_removals(requested: list[str], current: list[str], available: list[str]) -> list[str]:
    by_key = {label_key(label): label for label in [*available, *current]}
    return [by_key.get(label_key(value), value.strip()) for value in dedupe(requested)]


def plan_update(
    current: list[str],
    available: list[str],
    requested_add: list[str],
    requested_remove: list[str],
    exclusive_prefixes: list[str],
) -> dict[str, Any]:
    add = canonical_additions(requested_add, available)
    remove_requested = canonical_removals(requested_remove, current, available)
    remove_keys = {label_key(label) for label in remove_requested}
    conflicts = [label for label in add if label_key(label) in remove_keys]
    if conflicts:
        raise RuntimeError(f"same label requested for add and removal: {', '.join(conflicts)}")

    prefixes = dedupe(exclusive_prefixes)
    exclusive_targets: dict[str, str] = {}
    family_removals: list[str] = []
    for prefix in prefixes:
        prefix_key = label_key(prefix)
        targets = [label for label in add if label_key(label).startswith(prefix_key)]
        if len(targets) != 1:
            raise RuntimeError(
                f"exclusive prefix {prefix!r} requires exactly one matching --add target; found {targets}"
            )
        target = targets[0]
        exclusive_targets[prefix] = target
        family_removals.extend(
            label
            for label in current
            if label_key(label).startswith(prefix_key) and label_key(label) != label_key(target)
        )

    current_by_key = {label_key(label): label for label in current}
    remove_all = dedupe([*remove_requested, *family_removals])
    remove = [current_by_key[label_key(label)] for label in remove_all if label_key(label) in current_by_key]
    not_present = [label for label in remove_requested if label_key(label) not in current_by_key]
    actual_add = [label for label in add if label_key(label) not in current_by_key]

    remove_keys = {label_key(label) for label in remove}
    expected = [label for label in current if label_key(label) not in remove_keys]
    expected_keys = {label_key(label) for label in expected}
    for label in add:
        if label_key(label) not in expected_keys:
            expected.append(label)
            expected_keys.add(label_key(label))

    protected = [label for label in current if label_key(label) not in remove_keys]
    return {
        "requestedAdd": add,
        "requestedRemove": remove_requested,
        "add": actual_add,
        "remove": remove,
        "removeNotPresent": not_present,
        "exclusiveTargets": exclusive_targets,
        "protectedLabels": protected,
        "expectedLabels": expected,
        "changed": bool(actual_add or remove),
    }


def verify_after(before: list[str], after: list[str], plan: dict[str, Any]) -> None:
    after_keys = {label_key(label) for label in after}
    add_missing = [label for label in plan["requestedAdd"] if label_key(label) not in after_keys]
    remove_remaining = [label for label in plan["remove"] if label_key(label) in after_keys]
    protected_missing = [label for label in plan["protectedLabels"] if label_key(label) not in after_keys]
    exclusive_failures: dict[str, dict[str, Any]] = {}
    for prefix, target in plan["exclusiveTargets"].items():
        matches = [label for label in after if label_key(label).startswith(label_key(prefix))]
        if len(matches) != 1 or label_key(matches[0]) != label_key(target):
            exclusive_failures[prefix] = {"expected": target, "actual": matches}
    failures = {
        "missingAddedLabels": add_missing,
        "remainingRemovedLabels": remove_remaining,
        "missingProtectedLabels": protected_missing,
        "exclusiveFamilyFailures": exclusive_failures,
    }
    if any(failures.values()):
        raise RuntimeError(
            "label verification failed: "
            + json.dumps({"before": before, "after": after, **failures}, ensure_ascii=False)
        )


def apply_update(repo: str, pr: int, before: list[str], plan: dict[str, Any]) -> list[str]:
    try:
        if plan["add"]:
            api_json(
                f"repos/{repo}/issues/{pr}/labels",
                method="POST",
                body={"labels": plan["add"]},
            )
        for label in plan["remove"]:
            api_json(f"repos/{repo}/issues/{pr}/labels/{quote(label, safe='')}", method="DELETE")
    except (CommandError, RuntimeError) as exc:
        try:
            observed: list[str] | str = issue_labels(repo, pr)
        except (CommandError, RuntimeError) as observe_exc:
            observed = f"unavailable: {observe_exc}"
        raise RuntimeError(
            f"label update failed after a possible partial write: {exc}\n"
            f"observed labels: {json.dumps(observed, ensure_ascii=False)}"
        ) from exc
    after = issue_labels(repo, pr)
    verify_after(before, after, plan)
    return after


def parse_simulated(args: argparse.Namespace) -> tuple[list[str], list[dict[str, Any]]] | None:
    current_raw = args.simulate_current_json
    available_raw = args.simulate_available_json
    if current_raw is None and available_raw is None:
        return None
    if current_raw is None or available_raw is None:
        raise RuntimeError("simulation requires both --simulate-current-json and --simulate-available-json")
    if args.apply:
        raise RuntimeError("simulation cannot be used with --apply")
    current = json.loads(current_raw)
    available_names = json.loads(available_raw)
    if not isinstance(current, list) or not all(isinstance(item, str) for item in current):
        raise RuntimeError("--simulate-current-json must be a JSON array of strings")
    if not isinstance(available_names, list) or not all(isinstance(item, str) for item in available_names):
        raise RuntimeError("--simulate-available-json must be a JSON array of strings")
    available = [{"name": name, "color": "", "description": ""} for name in available_names]
    return current, available


def inspect_command(args: argparse.Namespace) -> dict[str, Any]:
    repo, pr = resolve_target(args.pr, args.repo, args.repo_dir)
    return {"action": "inspected", **inspect_pr(repo, pr)}


def update_command(args: argparse.Namespace) -> dict[str, Any]:
    if not args.add and not args.remove:
        raise RuntimeError("update requires at least one --add or --remove label")
    repo, pr = resolve_target(args.pr, args.repo, args.repo_dir)
    simulated = parse_simulated(args)
    if simulated is None:
        context = inspect_pr(repo, pr)
        before = context["currentLabels"]
        available = context["availableLabels"]
    else:
        before, available = simulated
        context = {
            "repo": repo,
            "pr": pr,
            "title": None,
            "url": None,
            "state": "simulated",
            "draft": None,
        }
    plan = plan_update(
        before,
        [item["name"] for item in available],
        args.add,
        args.remove,
        args.exclusive_prefix,
    )
    if args.apply and plan["changed"]:
        action = "updated"
        after = apply_update(repo, pr, before, plan)
    elif args.apply:
        action = "no-op"
        after = before
    else:
        action = "planned"
        after = None
    return {
        "action": action,
        **context,
        "dryRun": not args.apply,
        "mutationPerformed": action == "updated",
        "beforeLabels": before,
        "plan": plan,
        "afterLabels": after,
    }


def render_markdown(result: dict[str, Any]) -> str:
    if result["action"] == "inspected":
        lines = [
            "# PR labels: inspected",
            f"- PR: {result['repo']}#{result['pr']} — {result.get('title')}",
            f"- URL: {result.get('url')}",
            f"- State: {result.get('state')}; draft: {result.get('draft')}",
            f"- Current: {', '.join(result['currentLabels']) or '(none)'}",
            "\n## Available labels",
        ]
        for item in result["availableLabels"]:
            description = f" — {item['description']}" if item["description"] else ""
            lines.append(f"- `{item['name']}`{description}")
        return "\n".join(lines)

    plan = result["plan"]
    lines = [
        f"# PR labels: {result['action']}",
        f"- PR: {result['repo']}#{result['pr']}",
        f"- Before: {', '.join(result['beforeLabels']) or '(none)'}",
        f"- Add: {', '.join(plan['add']) or '(none)'}",
        f"- Remove: {', '.join(plan['remove']) or '(none)'}",
        f"- Requested removals already absent: {', '.join(plan['removeNotPresent']) or '(none)'}",
        f"- Expected: {', '.join(plan['expectedLabels']) or '(none)'}",
        f"- Changed: {plan['changed']}",
    ]
    if result["afterLabels"] is not None:
        lines.append(f"- Verified after: {', '.join(result['afterLabels']) or '(none)'}")
    else:
        lines.append("- GitHub mutation: not performed (dry run)")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect and safely update GitHub PR labels.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect = subparsers.add_parser("inspect", help="Read PR and repository labels")
    inspect.add_argument("pr", help="PR number or GitHub PR URL")
    inspect.add_argument("--repo", help="OWNER/REPO; inferred from URL or current repository")
    inspect.add_argument("--repo-dir", help="Repository path used when inferring --repo")
    inspect.add_argument("--format", choices=("json", "markdown"), default="json")
    inspect.set_defaults(func=inspect_command)

    update = subparsers.add_parser("update", help="Plan or apply a minimal PR label update")
    update.add_argument("pr", help="PR number or GitHub PR URL")
    update.add_argument("--repo", help="OWNER/REPO; inferred from URL or current repository")
    update.add_argument("--repo-dir", help="Repository path used when inferring --repo")
    update.add_argument("--add", action="append", default=[], help="Existing repository label to add")
    update.add_argument("--remove", action="append", default=[], help="Exact label to remove")
    update.add_argument(
        "--exclusive-prefix",
        action="append",
        default=[],
        help="Repository-defined exclusive family prefix; requires one matching --add",
    )
    update.add_argument("--apply", action="store_true", help="Perform and verify the planned mutation")
    update.add_argument("--format", choices=("json", "markdown"), default="json")
    update.add_argument("--simulate-current-json", help=argparse.SUPPRESS)
    update.add_argument("--simulate-available-json", help=argparse.SUPPRESS)
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
