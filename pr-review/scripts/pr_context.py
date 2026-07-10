#!/usr/bin/env python3
"""Compact GitHub PR context for pr-review skill.

Fetches metadata and CI/check rollup via gh, then emits a concise review gate
summary. It intentionally does not run local tests.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from typing import Any

FIELDS = [
    "number",
    "title",
    "state",
    "mergedAt",
    "isDraft",
    "author",
    "headRefName",
    "headRefOid",
    "baseRefName",
    "mergeable",
    "reviewDecision",
    "statusCheckRollup",
    "labels",
    "additions",
    "deletions",
    "changedFiles",
    "files",
    "commits",
    "url",
]

PASS_CONCLUSIONS = {"SUCCESS", "NEUTRAL"}
SKIP_CONCLUSIONS = {"SKIPPED"}
FAIL_CONCLUSIONS = {"FAILURE", "TIMED_OUT", "ACTION_REQUIRED", "CANCELLED", "STARTUP_FAILURE"}
PENDING_STATES = {"PENDING", "EXPECTED", "IN_PROGRESS", "QUEUED", "REQUESTED", "WAITING"}
PASS_STATES = {"SUCCESS", "PASSED"}
FAIL_STATES = {"FAILURE", "FAILED", "ERROR"}


def run_gh(args: list[str]) -> str:
    proc = subprocess.run(
        ["gh", *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        raise SystemExit(proc.returncode)
    return proc.stdout


def pr_view(pr: str, repo: str | None) -> dict[str, Any]:
    args = ["pr", "view", pr, "--json", ",".join(FIELDS)]
    if repo:
        args.extend(["--repo", repo])
    return json.loads(run_gh(args))


def label_names(labels: list[dict[str, Any]]) -> list[str]:
    return [str(label.get("name", "")) for label in labels if label.get("name")]


def check_name(item: dict[str, Any]) -> str:
    for key in ("name", "context", "workflowName"):
        value = item.get(key)
        if value:
            return str(value)
    app = item.get("app")
    if isinstance(app, dict) and app.get("name"):
        return str(app["name"])
    return item.get("__typename", "unknown")


def normalize_check(item: dict[str, Any]) -> tuple[str, str, str | None, str | None]:
    """Return bucket, name, state/status, conclusion."""
    name = check_name(item)
    conclusion = item.get("conclusion")
    state = item.get("state") or item.get("status")

    conclusion_u = str(conclusion).upper() if conclusion else None
    state_u = str(state).upper() if state else None

    if conclusion_u in PASS_CONCLUSIONS:
        return "pass", name, state_u, conclusion_u
    if conclusion_u in SKIP_CONCLUSIONS:
        return "skipped", name, state_u, conclusion_u
    if conclusion_u in FAIL_CONCLUSIONS:
        return "fail", name, state_u, conclusion_u
    if state_u in PASS_STATES:
        return "pass", name, state_u, conclusion_u
    if state_u in FAIL_STATES:
        return "fail", name, state_u, conclusion_u
    if state_u in PENDING_STATES:
        return "pending", name, state_u, conclusion_u
    return "unknown", name, state_u, conclusion_u


def summarize_ci(checks: list[dict[str, Any]]) -> dict[str, Any]:
    normalized = []
    counts: Counter[str] = Counter()
    for item in checks:
        bucket, name, state, conclusion = normalize_check(item)
        counts[bucket] += 1
        normalized.append(
            {
                "name": name,
                "bucket": bucket,
                "state": state,
                "conclusion": conclusion,
                "detailsUrl": item.get("detailsUrl") or item.get("targetUrl"),
            }
        )

    total = len(normalized)
    if total == 0:
        overall = "missing"
    elif counts["fail"]:
        overall = "failing"
    elif counts["pending"]:
        overall = "pending"
    elif counts["unknown"]:
        overall = "ambiguous"
    else:
        overall = "green"

    important = [c for c in normalized if c["bucket"] in {"fail", "pending", "unknown"}]
    return {
        "overall": overall,
        "total": total,
        "counts": dict(counts),
        "important": important[:12],
    }


def local_guidance(ci: dict[str, Any], is_merged: bool) -> str:
    overall = ci["overall"]
    prefix = "merged PR; use retrospective/read-only verification; " if is_merged else ""
    if overall == "green":
        return prefix + "remote CI is green; compare its matrix with the changed proof obligations before adding focused checks"
    if overall == "missing":
        return prefix + "remote CI is missing/unavailable; use focused local checks when the review needs behavior evidence"
    if overall == "failing":
        return prefix + "remote CI is failing; inspect failed checks first, then reproduce only decision-relevant failures"
    if overall == "pending":
        return prefix + "remote CI is pending; report or wait for it because local full CI is not a substitute for required checks"
    return prefix + "remote CI is ambiguous; inspect check details and changed proof obligations before choosing focused verification"


def summarize(data: dict[str, Any]) -> dict[str, Any]:
    is_merged = bool(data.get("mergedAt") or str(data.get("state", "")).upper() == "MERGED")
    ci = summarize_ci(data.get("statusCheckRollup") or [])
    return {
        "number": data.get("number"),
        "title": data.get("title"),
        "url": data.get("url"),
        "state": data.get("state"),
        "mergedAt": data.get("mergedAt"),
        "isMerged": is_merged,
        "reviewMode": "retrospective-read-only" if is_merged else "active-read-only",
        "isDraft": data.get("isDraft"),
        "author": (data.get("author") or {}).get("login"),
        "baseRefName": data.get("baseRefName"),
        "headRefName": data.get("headRefName"),
        "headRefOid": data.get("headRefOid"),
        "mergeable": data.get("mergeable"),
        "reviewDecision": data.get("reviewDecision"),
        "labels": label_names(data.get("labels") or []),
        "size": {
            "additions": data.get("additions"),
            "deletions": data.get("deletions"),
            "changedFiles": data.get("changedFiles"),
        },
        "ci": ci,
        "localVerificationGuidance": local_guidance(ci, is_merged),
        "files": [
            {
                "path": item.get("path"),
                "additions": item.get("additions"),
                "deletions": item.get("deletions"),
            }
            for item in data.get("files") or []
        ],
    }


def render_markdown(summary: dict[str, Any]) -> str:
    size = summary["size"]
    ci = summary["ci"]
    head = (summary.get("headRefOid") or "")[:8]
    lines = [
        f"# PR #{summary['number']} context",
        f"- Title: {summary.get('title')}",
        f"- URL: {summary.get('url')}",
        f"- State: {summary.get('state')}; mergedAt: {summary.get('mergedAt') or 'null'}; draft: {summary.get('isDraft')}",
        f"- Author: {summary.get('author')}",
        f"- Base <- head: {summary.get('baseRefName')} <- {summary.get('headRefName')} ({head})",
        f"- Mergeable: {summary.get('mergeable')}; reviewDecision: {summary.get('reviewDecision')}",
        f"- Size: +{size.get('additions')} / -{size.get('deletions')} across {size.get('changedFiles')} files",
        f"- Labels: {', '.join(summary.get('labels') or []) or '(none)'}",
        f"- Review mode: {summary.get('reviewMode')}",
        f"- CI: {ci['overall']} ({ci['total']} checks; {ci['counts']})",
    ]
    if ci["important"]:
        lines.append("- Non-green checks:")
        for item in ci["important"]:
            detail = f"state={item.get('state')} conclusion={item.get('conclusion')}"
            lines.append(f"  - {item['name']}: {item['bucket']} ({detail})")
    lines.append(f"- Local verification: {summary['localVerificationGuidance']}")
    lines.append("\n## Changed files")
    for item in summary["files"]:
        lines.append(f"- {item['path']} (+{item.get('additions')} / -{item.get('deletions')})")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize GitHub PR metadata and CI for review gating.")
    parser.add_argument("pr", help="PR number or URL accepted by gh pr view")
    parser.add_argument("--repo", help="OWNER/REPO; omitted means current gh repository context")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args()

    summary = summarize(pr_view(args.pr, args.repo))
    if args.format == "json":
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(summary))


if __name__ == "__main__":
    main()
