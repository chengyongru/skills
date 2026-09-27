#!/usr/bin/env python3
"""Open a Git worktree to the right of the calling Herdr pane on Linux."""

import argparse
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import time


def run_command(arguments):
    result = subprocess.run(
        arguments, capture_output=True, text=True, encoding="utf-8", timeout=15,
    )
    if result.returncode:
        raise RuntimeError(f"{arguments[0]} failed: {result.stderr.strip() or result.stdout.strip()}")
    return result.stdout


def herdr(*arguments, text=False):
    output = run_command(["herdr", *arguments])
    if text:
        return output
    response = json.loads(output)
    if response.get("error") or not isinstance(response.get("result"), dict):
        raise RuntimeError(f"Herdr returned no successful result: {output}")
    return response["result"]


def same_path(value, worktree):
    return (
        isinstance(value, str) and os.path.isabs(value)
        and os.path.normpath(value) == worktree
    )


def directory_command(shell, worktree):
    if any(character in worktree for character in "\r\n\x1b"):
        raise RuntimeError("Worktree path contains terminal control characters.")
    shell = Path(shell).name.removeprefix("-")
    if shell in {"bash", "zsh", "sh", "dash", "ksh"}:
        return f"cd -- {shlex.quote(worktree)}"
    if shell in {"pwsh", "powershell"}:
        return "Set-Location -LiteralPath '" + worktree.replace("'", "''") + "'"
    raise RuntimeError(f"Unsupported shell '{shell}' in right-hand pane.")


def open_worktree(cwd, dry_run=False):
    if os.environ.get("HERDR_ENV") != "1" or not os.environ.get("HERDR_PANE_ID"):
        raise RuntimeError("Run inside a Herdr pane with HERDR_ENV=1 and inherited HERDR_PANE_ID.")
    root = run_command(["git", "-C", cwd, "rev-parse", "--show-toplevel"]).rstrip("\n")
    if not os.path.isabs(root) or any(c in root for c in "\r\n\x1b"):
        raise RuntimeError("Git did not return a safe absolute worktree path.")
    worktree = os.path.normpath(root)
    caller = herdr("pane", "current", "--current")["pane"]
    if not caller.get("pane_id") or not caller.get("tab_id"):
        raise RuntimeError("Herdr did not resolve the calling pane.")
    neighbor = herdr(
        "pane", "neighbor", "--pane", caller["pane_id"], "--direction", "right",
    )["neighbor"]
    if (neighbor["pane_id"] != caller["pane_id"]
            or neighbor["layout"]["tab_id"] != caller["tab_id"]):
        raise RuntimeError("Herdr returned a neighbor for a different caller or tab.")
    target_id = neighbor.get("neighbor_pane_id")
    action = "reuse" if target_id else "create"
    command = None

    def get_target():
        pane = herdr("pane", "get", target_id)["pane"]
        if pane["pane_id"] != target_id or pane["tab_id"] != caller["tab_id"]:
            raise RuntimeError(f"Target pane changed identity or tab: {target_id}")
        return pane

    if target_id:
        if target_id == caller["pane_id"] or target_id not in {
            pane["pane_id"] for pane in neighbor["layout"]["panes"]
        }:
            raise RuntimeError("Herdr returned an invalid right-hand neighbor.")
        target = get_target()
        if not same_path(target.get("cwd"), worktree):
            process = herdr("pane", "process-info", "--pane", target_id)["process_info"]
            foreground = [item for item in process.get("foreground_processes", []) if item]
            if (target.get("agent") or process["pane_id"] != target_id
                    or not process.get("shell_pid") or len(foreground) != 1
                    or foreground[0]["pid"] != process["shell_pid"]):
                raise RuntimeError(f"Right-hand pane {target_id} is occupied or its shell is unknown.")
            command = directory_command(foreground[0]["name"], worktree)
            screen = herdr(
                "pane", "read", target_id, "--source", "recent-unwrapped", "--lines", "8",
                text=True,
            )
            lines = [line for line in screen.splitlines() if line.strip()]
            if not lines or not re.search(r"[>❯➜$#%]\s*$", lines[-1]):
                raise RuntimeError(f"Right-hand pane {target_id} has no recognizable empty prompt.")

    result = {"caller_pane_id": caller["pane_id"], "pane_id": target_id, "worktree": worktree}
    if dry_run:
        return dict(result, status="dry-run", action=action, change_directory=bool(command))

    if action == "create":
        created = herdr(
            "pane", "split", "--pane", caller["pane_id"], "--direction", "right",
            "--cwd", worktree, "--no-focus",
        )["pane"]
        target_id = created.get("pane_id")
        if (not target_id or target_id == caller["pane_id"]
                or created["tab_id"] != caller["tab_id"]):
            raise RuntimeError("Herdr did not return a valid new pane in the calling tab.")
    elif command:
        herdr("pane", "run", target_id, command, text=True)

    deadline = time.monotonic() + 5
    while True:
        target = get_target()
        if same_path(target.get("cwd"), worktree):
            return dict(result, pane_id=target_id, status="created" if action == "create" else "reused")
        if time.monotonic() >= deadline:
            raise RuntimeError(
                f"Pane {target_id} did not report worktree '{worktree}' within five seconds; "
                f"current cwd: {target.get('cwd')}. Keep the pane for inspection."
            )
        time.sleep(0.2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cwd", default=os.getcwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(open_worktree(args.cwd, args.dry_run), ensure_ascii=False))
    except (OSError, RuntimeError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        print(json.dumps({"status": "error", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
