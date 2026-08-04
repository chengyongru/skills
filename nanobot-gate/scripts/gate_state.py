#!/usr/bin/env python3
"""Track snapshot-bound nanobot gate results."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

GATES = ("simplify", "verify", "candidate-review", "pr-review", "remote-ci")
NON_CARRYABLE_GATES = {"candidate-review", "pr-review", "remote-ci"}
REMOTE_BOUND_GATES = {"pr-review", "remote-ci"}
RECORDABLE_STATUSES = ("PASS", "WARN", "FAIL", "BLOCKED", "NOT_RUN")
CARRYABLE_STATUSES = ("PASS", "WARN", "NOT_RUN")
SCHEMA_VERSION = 1


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_git(repo: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        message = result.stderr.decode(errors="replace").strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {message}")
    return result.stdout


def resolve_repo(repo: str | Path) -> Path:
    requested = Path(repo).expanduser().resolve()
    root = run_git(requested, "rev-parse", "--show-toplevel").decode().strip()
    return Path(root).resolve()


def hash_file(digest: Any, path: Path) -> None:
    if path.is_symlink():
        digest.update(b"symlink\0")
        digest.update(os.fsencode(os.readlink(path)))
        return
    if not path.is_file():
        digest.update(b"missing-or-special\0")
        return
    digest.update(b"file\0")
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)


def build_snapshot(repo: str | Path, base_ref: str) -> dict[str, Any]:
    root = resolve_repo(repo)
    base_oid = (
        run_git(root, "rev-parse", "--verify", f"{base_ref}^{{commit}}")
        .decode()
        .strip()
    )
    head_oid = run_git(root, "rev-parse", "HEAD").decode().strip()
    diff = run_git(root, "diff", "--binary", "--no-ext-diff", base_ref, "--")
    tracked_raw = run_git(root, "diff", "--name-only", "-z", base_ref, "--")
    untracked_raw = run_git(
        root,
        "-c",
        "core.quotepath=false",
        "ls-files",
        "--others",
        "--exclude-standard",
        "-z",
    )
    untracked = sorted(item for item in untracked_raw.split(b"\0") if item)

    digest = hashlib.sha256()
    digest.update(b"nanobot-gate-candidate-v1\0")
    digest.update(base_oid.encode())
    digest.update(b"\0diff\0")
    digest.update(diff)
    for raw_path in untracked:
        digest.update(b"\0untracked-path\0")
        digest.update(raw_path)
        digest.update(b"\0content\0")
        hash_file(digest, root / os.fsdecode(raw_path))

    tracked = [os.fsdecode(item) for item in tracked_raw.split(b"\0") if item]
    untracked_text = [os.fsdecode(item) for item in untracked]
    return {
        "repo": str(root),
        "base_ref": base_ref,
        "base_oid": base_oid,
        "head_oid": head_oid,
        "candidate_id": digest.hexdigest(),
        "changed_paths": sorted(set(tracked + untracked_text)),
        "captured_at": now(),
    }


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise RuntimeError(f"state file does not exist: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != SCHEMA_VERSION:
        raise RuntimeError(f"unsupported state schema: {data.get('schema_version')!r}")
    return data


def write_state(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    temp.replace(path)


def snapshot_command(args: argparse.Namespace) -> int:
    state_path = Path(args.state).expanduser().resolve()
    snapshot = build_snapshot(args.repo, args.base)
    carries = set(args.carry or [])
    if carries and not args.reason:
        raise RuntimeError("--reason is required when --carry is used")

    if state_path.exists():
        data = load_state(state_path)
        old_snapshot = data["candidate"]
        old_id = old_snapshot["candidate_id"]
        changed = old_id != snapshot["candidate_id"]
        invalidated: list[str] = []
        carried: list[str] = []

        if changed:
            if old_snapshot["base_oid"] != snapshot["base_oid"] and carries:
                raise RuntimeError(
                    "gate results cannot be carried across a base commit change"
                )
            forbidden_carries = carries & NON_CARRYABLE_GATES
            if forbidden_carries:
                raise RuntimeError(
                    "review/remote gates cannot be carried across candidate changes: "
                    + ", ".join(sorted(forbidden_carries))
                )
            gates = data.setdefault("gates", {})
            unknown = carries - gates.keys()
            if unknown:
                raise RuntimeError(
                    "cannot carry unrecorded gate(s): " + ", ".join(sorted(unknown))
                )
            for gate, result in gates.items():
                status = result.get("status")
                if gate in carries:
                    if status not in CARRYABLE_STATUSES:
                        raise RuntimeError(
                            f"cannot carry {gate} with status {status!r}"
                        )
                    result["carried_from_candidate_id"] = result.get("candidate_id")
                    result["candidate_id"] = snapshot["candidate_id"]
                    result["carry_reason"] = args.reason
                    result["updated_at"] = now()
                    carried.append(gate)
                else:
                    result["previous_status"] = status
                    result["status"] = "STALE"
                    result["stale_reason"] = (
                        f"candidate changed from {old_id} to {snapshot['candidate_id']}"
                    )
                    result["updated_at"] = now()
                    invalidated.append(gate)
            data.setdefault("history", []).append(
                {
                    "event": "candidate_changed",
                    "at": now(),
                    "old_candidate_id": old_id,
                    "new_candidate_id": snapshot["candidate_id"],
                    "invalidated": invalidated,
                    "carried": carried,
                    "carry_reason": args.reason if carried else None,
                }
            )
        else:
            invalidated = []
            carried = []
            data.setdefault("history", []).append(
                {
                    "event": "snapshot_refreshed",
                    "at": now(),
                    "candidate_id": snapshot["candidate_id"],
                    "head_oid": snapshot["head_oid"],
                }
            )
        data["candidate"] = snapshot
        data["updated_at"] = now()
    else:
        if carries:
            raise RuntimeError("--carry cannot be used for the first snapshot")
        data = {
            "schema_version": SCHEMA_VERSION,
            "created_at": now(),
            "updated_at": now(),
            "candidate": snapshot,
            "gates": {},
            "history": [
                {
                    "event": "snapshot_created",
                    "at": now(),
                    "candidate_id": snapshot["candidate_id"],
                }
            ],
        }
        changed = True
        invalidated = []
        carried = []

    write_state(state_path, data)
    print(
        json.dumps(
            {
                "state": str(state_path),
                "candidate_id": snapshot["candidate_id"],
                "head_oid": snapshot["head_oid"],
                "base_oid": snapshot["base_oid"],
                "changed": changed,
                "invalidated": invalidated,
                "carried": carried,
            },
            indent=2,
        )
    )
    return 0


def assert_current(data: dict[str, Any]) -> dict[str, Any]:
    expected = data["candidate"]
    current = build_snapshot(expected["repo"], expected["base_ref"])
    if current["candidate_id"] != expected["candidate_id"]:
        raise RuntimeError(
            "candidate content changed; run snapshot before recording or checking gates"
        )
    if current["base_oid"] != expected["base_oid"]:
        raise RuntimeError(
            "base commit changed; run snapshot before recording or checking gates"
        )
    return current


def record_command(args: argparse.Namespace) -> int:
    state_path = Path(args.state).expanduser().resolve()
    data = load_state(state_path)
    current = assert_current(data)
    if args.status in {"PASS", "WARN", "FAIL"} and not args.evidence:
        raise RuntimeError(f"{args.status} requires at least one --evidence path")
    if (
        args.gate in REMOTE_BOUND_GATES
        and args.status in {"PASS", "WARN", "FAIL"}
        and not args.remote_head
    ):
        raise RuntimeError(f"{args.gate} results require --remote-head")
    previous = data.setdefault("gates", {}).get(args.gate, {})
    required = (
        args.required
        if args.required is not None
        else bool(previous.get("required", True))
    )
    result = {
        "status": args.status,
        "required": required,
        "candidate_id": current["candidate_id"],
        "head_oid": current["head_oid"],
        "remote_head": args.remote_head,
        "evidence": args.evidence or [],
        "judgment": args.judgment,
        "updated_at": now(),
    }
    data["gates"][args.gate] = result
    data["updated_at"] = now()
    data.setdefault("history", []).append(
        {
            "event": "gate_recorded",
            "at": now(),
            "gate": args.gate,
            "status": args.status,
            "candidate_id": current["candidate_id"],
            "required": required,
        }
    )
    write_state(state_path, data)
    print(json.dumps({"gate": args.gate, **result}, indent=2))
    return 0


def check_command(args: argparse.Namespace) -> int:
    state_path = Path(args.state).expanduser().resolve()
    data = load_state(state_path)
    current = assert_current(data)
    required = args.required or [
        gate for gate, result in data.get("gates", {}).items() if result.get("required")
    ]
    if not required:
        raise RuntimeError("no required gates were declared")

    statuses: dict[str, str] = {}
    for gate in required:
        result = data.get("gates", {}).get(gate)
        if not result:
            statuses[gate] = "STALE"
            continue
        if result.get("candidate_id") != current["candidate_id"]:
            statuses[gate] = "STALE"
            continue
        statuses[gate] = result.get("status", "STALE")

    values = set(statuses.values())
    if "FAIL" in values:
        outcome, exit_code = "FAIL", 1
    elif "BLOCKED" in values or "NOT_RUN" in values:
        outcome, exit_code = "BLOCKED", 2
    elif "STALE" in values:
        outcome, exit_code = "STALE", 3
    elif "WARN" in values:
        outcome, exit_code = "WARN", 4
    elif values == {"PASS"}:
        outcome, exit_code = "PASS", 0
    else:
        outcome, exit_code = "BLOCKED", 2

    print(
        json.dumps(
            {
                "outcome": outcome,
                "candidate_id": current["candidate_id"],
                "head_oid": current["head_oid"],
                "required_gates": statuses,
            },
            indent=2,
        )
    )
    return exit_code


def show_command(args: argparse.Namespace) -> int:
    data = load_state(Path(args.state).expanduser().resolve())
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    snapshot = commands.add_parser("snapshot", help="Create or refresh candidate state")
    snapshot.add_argument("--repo", required=True)
    snapshot.add_argument("--base", required=True)
    snapshot.add_argument("--state", required=True)
    snapshot.add_argument("--carry", action="append", choices=GATES)
    snapshot.add_argument("--reason")
    snapshot.set_defaults(func=snapshot_command)

    record = commands.add_parser("record", help="Record a gate result")
    record.add_argument("--state", required=True)
    record.add_argument("--gate", required=True, choices=GATES)
    record.add_argument("--status", required=True, choices=RECORDABLE_STATUSES)
    required_group = record.add_mutually_exclusive_group()
    required_group.add_argument("--required", dest="required", action="store_true")
    required_group.add_argument("--optional", dest="required", action="store_false")
    record.set_defaults(required=None)
    record.add_argument("--evidence", action="append")
    record.add_argument("--judgment", required=True)
    record.add_argument("--remote-head")
    record.set_defaults(func=record_command)

    check = commands.add_parser("check", help="Check required gate readiness")
    check.add_argument("--state", required=True)
    check.add_argument("--required", nargs="+", choices=GATES)
    check.set_defaults(func=check_command)

    show = commands.add_parser("show", help="Print the state manifest")
    show.add_argument("--state", required=True)
    show.set_defaults(func=show_command)
    return root


def main() -> int:
    try:
        args = parser().parse_args()
        return int(args.func(args))
    except (OSError, RuntimeError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
