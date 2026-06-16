#!/usr/bin/env python3
"""Manage PR audit state for PR audit sweeps.

The default policy is once-per-PR-number. A changed head SHA does not cause a
new audit unless the caller passes --force or clears the PR entry.
"""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_STATE = Path(".nanobot") / "pr-audit-state.json"
VERSION = 1
FINAL_STATES = {"reviewed", "skipped", "failed"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_iso(value: str, field: str) -> datetime:
    raw = value.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError as exc:
        raise SystemExit(f"Error: invalid ISO datetime for {field}: {value}") from exc
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).replace(microsecond=0)


def normalize_iso(value: str, field: str) -> str:
    return parse_iso(value, field).isoformat()


def empty_state() -> dict[str, Any]:
    return {
        "version": VERSION,
        "policy": {"mode": "once_per_pr"},
        "prs": {},
    }


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return empty_state()
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Error: invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"Error: state file {path} must contain a JSON object")
    data.setdefault("version", VERSION)
    data.setdefault("policy", {"mode": "once_per_pr"})
    data.setdefault("prs", {})
    if not isinstance(data["prs"], dict):
        raise SystemExit(f"Error: state file {path} has non-object 'prs'")
    return data


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=path.name + ".",
        suffix=".tmp",
        dir=str(path.parent),
        text=True,
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            json.dump(state, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
        try:
            dir_fd = os.open(path.parent, os.O_RDONLY)
        except OSError:
            return
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
    finally:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass


def pr_key(pr: int) -> str:
    if pr <= 0:
        raise SystemExit("Error: --pr must be a positive integer")
    return str(pr)


def get_entry(state: dict[str, Any], pr: int) -> dict[str, Any] | None:
    entry = state["prs"].get(pr_key(pr))
    if entry is None:
        return None
    if not isinstance(entry, dict):
        raise SystemExit(f"Error: PR {pr} entry is not an object")
    return entry


def set_entry(state: dict[str, Any], pr: int, entry: dict[str, Any]) -> None:
    state["prs"][pr_key(pr)] = entry


def base_entry(args: argparse.Namespace, status: str) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "pr": args.pr,
        "status": status,
        "updated_at": now_iso(),
    }
    if getattr(args, "head_sha", None):
        entry["head_sha"] = args.head_sha
    if getattr(args, "title", None):
        entry["title"] = args.title
    if getattr(args, "url", None):
        entry["url"] = args.url
    if getattr(args, "created_at", None):
        entry["created_at"] = normalize_iso(args.created_at, "--created-at")
    return entry


def print_json(obj: Any) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True))


def policy_skip(state: dict[str, Any], args: argparse.Namespace) -> dict[str, Any] | None:
    policy = state.setdefault("policy", {"mode": "once_per_pr"})
    min_pr = policy.get("min_pr_number")
    if min_pr is not None:
        if not isinstance(min_pr, int):
            raise SystemExit("Error: policy.min_pr_number must be an integer")
        if args.pr < min_pr:
            return {
                "pr": args.pr,
                "should_audit": False,
                "reason": "before_min_pr_number",
                "min_pr_number": min_pr,
            }

    created_after = policy.get("created_after")
    if created_after:
        if not isinstance(created_after, str):
            raise SystemExit("Error: policy.created_after must be an ISO datetime string")
        if not getattr(args, "created_at", ""):
            return {
                "pr": args.pr,
                "should_audit": False,
                "reason": "missing_created_at_for_cutoff",
                "created_after": created_after,
            }
        created_at_dt = parse_iso(args.created_at, "--created-at")
        created_after_dt = parse_iso(created_after, "policy.created_after")
        if created_at_dt < created_after_dt:
            return {
                "pr": args.pr,
                "should_audit": False,
                "reason": "before_created_after_cutoff",
                "created_at": created_at_dt.isoformat(),
                "created_after": created_after_dt.isoformat(),
            }
    return None


def cmd_should_audit(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    entry = get_entry(state, args.pr)
    if args.force:
        print_json(
            {
                "pr": args.pr,
                "should_audit": True,
                "reason": "forced",
                "existing": entry,
            }
        )
        return 0
    if skip := policy_skip(state, args):
        print_json(skip)
        return 0
    if entry and entry.get("status") in FINAL_STATES:
        print_json(
            {
                "pr": args.pr,
                "should_audit": False,
                "reason": "already_audited_once",
                "status": entry.get("status"),
                "audited_head_sha": entry.get("head_sha"),
                "current_head_sha": args.head_sha,
            }
        )
        return 0
    if entry and entry.get("status") == "in_progress":
        print_json(
            {
                "pr": args.pr,
                "should_audit": False,
                "reason": "audit_in_progress",
                "started_at": entry.get("started_at"),
                "head_sha": entry.get("head_sha"),
            }
        )
        return 0
    print_json({"pr": args.pr, "should_audit": True, "reason": "not_seen"})
    return 0


def cmd_mark_started(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    existing = get_entry(state, args.pr)
    if existing and existing.get("status") in FINAL_STATES and not args.force:
        print_json(
            {
                "pr": args.pr,
                "changed": False,
                "reason": "already_audited_once",
                "existing": existing,
            }
        )
        return 0
    entry = base_entry(args, "in_progress")
    entry["started_at"] = now_iso()
    if existing:
        entry["previous"] = existing
    set_entry(state, args.pr, entry)
    save_state(args.state, state)
    print_json({"pr": args.pr, "changed": True, "entry": entry})
    return 0


def finish_entry(args: argparse.Namespace, status: str) -> dict[str, Any]:
    state = load_state(args.state)
    existing = get_entry(state, args.pr) or {}
    entry = dict(existing)
    entry.update(base_entry(args, status))
    entry["completed_at"] = now_iso()
    if getattr(args, "verdict", None):
        entry["verdict"] = args.verdict
    if getattr(args, "reason", None):
        entry["reason"] = args.reason
    labels = getattr(args, "label", None) or []
    if labels:
        entry["labels"] = sorted(set(labels))
    if getattr(args, "review_url", None):
        entry["review_url"] = args.review_url
    if getattr(args, "notes", None):
        entry["notes"] = args.notes
    set_entry(state, args.pr, entry)
    save_state(args.state, state)
    return entry


def cmd_mark_reviewed(args: argparse.Namespace) -> int:
    entry = finish_entry(args, "reviewed")
    print_json({"pr": args.pr, "changed": True, "entry": entry})
    return 0


def cmd_mark_skipped(args: argparse.Namespace) -> int:
    entry = finish_entry(args, "skipped")
    print_json({"pr": args.pr, "changed": True, "entry": entry})
    return 0


def cmd_mark_failed(args: argparse.Namespace) -> int:
    entry = finish_entry(args, "failed")
    print_json({"pr": args.pr, "changed": True, "entry": entry})
    return 0


def cmd_get(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    entry = get_entry(state, args.pr)
    print_json(entry or {})
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    prs = state.get("prs", {})
    if args.status:
        prs = {
            key: value
            for key, value in prs.items()
            if isinstance(value, dict) and value.get("status") == args.status
        }
    print_json({"state": str(args.state), "prs": prs})
    return 0


def cmd_clear(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    existed = pr_key(args.pr) in state["prs"]
    state["prs"].pop(pr_key(args.pr), None)
    save_state(args.state, state)
    print_json({"pr": args.pr, "changed": existed})
    return 0


def cmd_set_policy(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    policy = state.setdefault("policy", {"mode": "once_per_pr"})
    policy["mode"] = "once_per_pr"
    changed = False

    if args.clear_created_after:
        changed = changed or "created_after" in policy
        policy.pop("created_after", None)
    if args.clear_min_pr_number:
        changed = changed or "min_pr_number" in policy
        policy.pop("min_pr_number", None)
    if args.created_after:
        normalized = normalize_iso(args.created_after, "--created-after")
        changed = changed or policy.get("created_after") != normalized
        policy["created_after"] = normalized
    if args.min_pr_number is not None:
        if args.min_pr_number <= 0:
            raise SystemExit("Error: --min-pr-number must be a positive integer")
        changed = changed or policy.get("min_pr_number") != args.min_pr_number
        policy["min_pr_number"] = args.min_pr_number

    if changed:
        save_state(args.state, state)
    print_json({"changed": changed, "policy": policy, "state": str(args.state)})
    return 0


def cmd_policy(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    print_json({"policy": state.get("policy", {}), "state": str(args.state)})
    return 0


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE, help="Audit state JSON path")


def add_pr_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--pr", type=int, required=True, help="PR number")
    parser.add_argument("--head-sha", default="", help="Current PR head SHA")
    parser.add_argument("--created-at", default="", help="PR createdAt ISO datetime")
    parser.add_argument("--title", default="", help="PR title")
    parser.add_argument("--url", default="", help="PR URL")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    add_common(parser)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("should-audit", help="Return whether a PR should be audited")
    add_pr_common(p)
    p.add_argument("--force", action="store_true", help="Ignore prior state")
    p.set_defaults(func=cmd_should_audit)

    p = sub.add_parser("mark-started", help="Mark a PR audit as started")
    add_pr_common(p)
    p.add_argument("--force", action="store_true", help="Overwrite final state")
    p.set_defaults(func=cmd_mark_started)

    p = sub.add_parser("mark-reviewed", help="Mark a PR audit as reviewed")
    add_pr_common(p)
    p.add_argument("--verdict", required=True, help="Review verdict")
    p.add_argument("--label", action="append", default=[], help="Applied label; repeatable")
    p.add_argument("--review-url", default="", help="Published or pending review URL")
    p.add_argument("--notes", default="", help="Short audit notes")
    p.set_defaults(func=cmd_mark_reviewed)

    p = sub.add_parser("mark-skipped", help="Mark a PR as skipped")
    add_pr_common(p)
    p.add_argument("--reason", required=True, help="Skip reason")
    p.add_argument("--notes", default="", help="Short notes")
    p.set_defaults(func=cmd_mark_skipped)

    p = sub.add_parser("mark-failed", help="Mark a PR audit as failed")
    add_pr_common(p)
    p.add_argument("--reason", required=True, help="Failure reason")
    p.add_argument("--notes", default="", help="Short notes")
    p.set_defaults(func=cmd_mark_failed)

    p = sub.add_parser("get", help="Print one PR entry")
    p.add_argument("--pr", type=int, required=True, help="PR number")
    p.set_defaults(func=cmd_get)

    p = sub.add_parser("list", help="Print state entries")
    p.add_argument("--status", choices=["in_progress", "reviewed", "skipped", "failed"])
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("clear", help="Clear one PR entry for explicit re-audit")
    p.add_argument("--pr", type=int, required=True, help="PR number")
    p.set_defaults(func=cmd_clear)

    p = sub.add_parser("set-policy", help="Set audit cutoff policy")
    p.add_argument("--created-after", default="", help="Audit only PRs created at or after this ISO datetime")
    p.add_argument("--min-pr-number", type=int, help="Audit only PRs with number greater than or equal to this")
    p.add_argument("--clear-created-after", action="store_true", help="Remove created_after cutoff")
    p.add_argument("--clear-min-pr-number", action="store_true", help="Remove min_pr_number cutoff")
    p.set_defaults(func=cmd_set_policy)

    p = sub.add_parser("policy", help="Print current audit policy")
    p.set_defaults(func=cmd_policy)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
