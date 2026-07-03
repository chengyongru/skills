#!/usr/bin/env python3
"""Set exactly one GitHub PR priority label via the REST issue-label API.

The script only manages labels matching ``priority: p*``. It preserves every
non-priority label and never adds ``valid``.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any
from urllib.parse import quote

PRIORITY_LABELS = {
    "p0": "priority: p0",
    "p1": "priority: p1",
    "p2": "priority: p2",
}
PRIORITY_RE = re.compile(r"^priority:\s*p\d+$", re.IGNORECASE)


def normalize_priority(value: str) -> str:
    raw = value.strip().lower()
    if raw.startswith("priority:"):
        raw = raw.split(":", 1)[1].strip()
    raw = raw.replace(" ", "")
    if raw in PRIORITY_LABELS:
        return PRIORITY_LABELS[raw]
    allowed = ", ".join(PRIORITY_LABELS.values())
    raise SystemExit(f"unsupported priority {value!r}; use one of: {allowed}")


def is_priority_label(label: str) -> bool:
    return bool(PRIORITY_RE.match(label.strip()))


def split_repo(repo: str) -> tuple[str, str]:
    parts = repo.strip().split("/", 1)
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise SystemExit("--repo must be OWNER/REPO")
    return parts[0], parts[1]


def run_gh_api(path: str, *, method: str = "GET", body: dict[str, Any] | None = None) -> str:
    env = dict(os.environ)
    env.setdefault("NO_COLOR", "1")
    args = ["gh", "api", path]
    if method != "GET":
        args.extend(["-X", method])

    tmp_path: Path | None = None
    try:
        if body is not None:
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as tmp:
                json.dump(body, tmp, ensure_ascii=False)
                tmp_path = Path(tmp.name)
            args.extend(["--input", str(tmp_path)])

        proc = subprocess.run(
            args,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            check=False,
        )
    finally:
        if tmp_path is not None:
            try:
                tmp_path.unlink()
            except FileNotFoundError:
                pass

    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        raise SystemExit(proc.returncode)
    return proc.stdout


def get_issue_labels(repo: str, pr: int) -> list[str]:
    payload = json.loads(run_gh_api(f"repos/{repo}/issues/{pr}"))
    labels = payload.get("labels") or []
    return [str(item.get("name", "")) for item in labels if item.get("name")]


def plan_priority_update(current_labels: list[str], target: str) -> dict[str, Any]:
    priority_labels = [label for label in current_labels if is_priority_label(label)]
    non_priority_labels = [label for label in current_labels if not is_priority_label(label)]
    remove = [label for label in priority_labels if label != target]
    add = target not in priority_labels
    planned = [*non_priority_labels, target]
    return {
        "target": target,
        "currentPriorityLabels": priority_labels,
        "removePriorityLabels": remove,
        "addPriorityLabel": target if add else None,
        "plannedLabels": planned,
    }


def apply_priority_update(repo: str, pr: int, plan: dict[str, Any]) -> None:
    for label in plan["removePriorityLabels"]:
        encoded = quote(label, safe="")
        run_gh_api(f"repos/{repo}/issues/{pr}/labels/{encoded}", method="DELETE")
    if plan["addPriorityLabel"]:
        run_gh_api(
            f"repos/{repo}/issues/{pr}/labels",
            method="POST",
            body={"labels": [plan["addPriorityLabel"]]},
        )


def validate_after(after_labels: list[str], target: str) -> None:
    priorities = [label for label in after_labels if is_priority_label(label)]
    if priorities != [target]:
        raise SystemExit(
            "priority label verification failed: "
            + json.dumps({"expected": [target], "actual": priorities}, ensure_ascii=False)
        )


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# Priority label: {'DRY RUN' if result['dryRun'] else 'UPDATED'}",
        f"- PR: {result['repo']}#{result['pr']}",
        f"- Target: `{result['target']}`",
        f"- Before: {', '.join(result['beforeLabels']) or '(none)'}",
        f"- Removed priority labels: {', '.join(result['removedPriorityLabels']) or '(none)'}",
        f"- Added priority label: {result['addedPriorityLabel'] or '(none)'}",
    ]
    if result["dryRun"]:
        lines.append(f"- Planned labels: {', '.join(result['plannedLabels']) or '(none)'}")
    else:
        lines.append(f"- After: {', '.join(result['afterLabels']) or '(none)'}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Set exactly one PR priority label via GitHub REST labels API.")
    parser.add_argument("pr", type=int, help="PR number")
    parser.add_argument("--repo", required=True, help="OWNER/REPO")
    parser.add_argument("--priority", required=True, help="p0, p1, p2, or full label name such as 'priority: p1'")
    parser.add_argument("--dry-run", action="store_true", help="Print the planned label changes without writing")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument(
        "--simulate-labels-json",
        help="Testing only: JSON array of current labels; implies no GitHub read and requires --dry-run",
    )
    args = parser.parse_args()

    split_repo(args.repo)
    target = normalize_priority(args.priority)

    if args.simulate_labels_json:
        if not args.dry_run:
            raise SystemExit("--simulate-labels-json requires --dry-run")
        raw_labels = json.loads(args.simulate_labels_json)
        if not isinstance(raw_labels, list) or not all(isinstance(item, str) for item in raw_labels):
            raise SystemExit("--simulate-labels-json must be a JSON array of strings")
        before = raw_labels
    else:
        before = get_issue_labels(args.repo, args.pr)

    plan = plan_priority_update(before, target)
    if args.dry_run:
        after = before
    else:
        apply_priority_update(args.repo, args.pr, plan)
        after = get_issue_labels(args.repo, args.pr)
        validate_after(after, target)

    result = {
        "repo": args.repo,
        "pr": args.pr,
        "target": target,
        "dryRun": args.dry_run,
        "beforeLabels": before,
        "removedPriorityLabels": plan["removePriorityLabels"],
        "addedPriorityLabel": plan["addPriorityLabel"],
        "plannedLabels": plan["plannedLabels"],
        "afterLabels": after,
    }
    if args.format == "markdown":
        print(render_markdown(result))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
