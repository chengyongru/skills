#!/usr/bin/env python3
"""Deterministic lifecycle helper for nanobot WebUI verification runs."""

from __future__ import annotations

import argparse
import ctypes
import json
import os
import re
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import uuid
from ctypes import wintypes
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

RUNTIME_ROOT = (Path(tempfile.gettempdir()) / "nanobot-webui-verify").resolve()
MANIFEST_NAME = "runtime-manifest.json"
EVIDENCE_PREFIX = ".verify-evidence-"


class LifecycleError(RuntimeError):
    """An expected, user-actionable lifecycle failure."""


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _load_manifest(path: Path) -> dict[str, Any]:
    path = path.resolve()
    if not path.is_file():
        raise LifecycleError(f"manifest not found: {path}")
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LifecycleError(f"invalid manifest {path}: {exc}") from exc
    if manifest.get("schema_version") != 1:
        raise LifecycleError(
            f"unsupported manifest schema: {manifest.get('schema_version')!r}"
        )
    return manifest


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def _validated_repo(value: str) -> Path:
    repo = Path(value).resolve()
    if not (repo / "nanobot").is_dir() or not (repo / "webui").is_dir():
        raise LifecycleError(f"not a nanobot repository root: {repo}")
    return repo


def _validated_evidence(repo: Path, value: str) -> Path:
    evidence = Path(value).resolve()
    webui = (repo / "webui").resolve()
    if not _is_within(evidence, webui) or evidence.parent == evidence:
        raise LifecycleError(f"evidence directory must be inside {webui}: {evidence}")
    if not evidence.name.startswith(EVIDENCE_PREFIX):
        raise LifecycleError(
            f"evidence directory name must start with {EVIDENCE_PREFIX!r}: {evidence.name}"
        )
    return evidence


def _validated_run_id(value: str | None) -> str:
    run_id = value or f"{os.getpid()}-{uuid.uuid4().hex[:8]}"
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", run_id):
        raise LifecycleError(
            "run id must be 1-64 letters, digits, dots, underscores, or hyphens"
        )
    return run_id


def _validated_runtime(value: str) -> Path:
    runtime = Path(value).resolve()
    if runtime == RUNTIME_ROOT or not _is_within(runtime, RUNTIME_ROOT):
        raise LifecycleError(
            f"refusing runtime path outside fixed root {RUNTIME_ROOT}: {runtime}"
        )
    return runtime


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.bind(("127.0.0.1", 0))
        return int(listener.getsockname()[1])


def _port_in_use(port: int) -> bool:
    """Check ownership without sending malformed traffic to the HTTP/WebSocket server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        try:
            probe.bind(("127.0.0.1", port))
        except OSError:
            return True
    return False


def _pid_running(pid: int) -> bool:
    if pid <= 0:
        return False
    if os.name == "nt":
        process_query_limited_information = 0x1000
        still_active = 259
        kernel32 = ctypes.windll.kernel32
        kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        kernel32.OpenProcess.restype = wintypes.HANDLE
        kernel32.GetExitCodeProcess.argtypes = [
            wintypes.HANDLE,
            ctypes.POINTER(wintypes.DWORD),
        ]
        kernel32.GetExitCodeProcess.restype = wintypes.BOOL
        kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel32.CloseHandle.restype = wintypes.BOOL
        handle = kernel32.OpenProcess(process_query_limited_information, False, pid)
        if not handle:
            return False
        try:
            exit_code = wintypes.DWORD()
            return bool(
                kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code))
            ) and (exit_code.value == still_active)
        finally:
            kernel32.CloseHandle(handle)
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def _process_command(pid: int) -> str | None:
    if not _pid_running(pid):
        return None
    if os.name == "nt":
        command = (
            '$p = Get-CimInstance Win32_Process -Filter "ProcessId = '
            f'{pid}"; if ($p) {{ $p.CommandLine }}'
        )
        result = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", command],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        return result.stdout.strip() or None
    proc_cmdline = Path(f"/proc/{pid}/cmdline")
    if proc_cmdline.is_file():
        try:
            return (
                proc_cmdline.read_bytes()
                .replace(b"\0", b" ")
                .decode(errors="replace")
                .strip()
            )
        except OSError:
            pass
    result = subprocess.run(
        ["ps", "-p", str(pid), "-o", "command="],
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    return result.stdout.strip() or None


def _process_matches(pid: int, config_path: Path) -> bool:
    command = _process_command(pid)
    if not command:
        return False
    normalized = command.casefold().replace("\\", "/")
    expected = str(config_path.resolve()).casefold().replace("\\", "/")
    return (
        expected in normalized and "nanobot" in normalized and "gateway" in normalized
    )


def _terminate_tree(pid: int, config_path: Path) -> list[str]:
    warnings: list[str] = []
    if not _pid_running(pid):
        return warnings
    if not _process_matches(pid, config_path):
        raise LifecycleError(
            f"refusing to stop PID {pid}: command line does not match gateway config {config_path}"
        )
    if os.name == "nt":
        result = subprocess.run(
            ["taskkill", "/PID", str(pid), "/T", "/F"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        if result.returncode and _pid_running(pid):
            raise LifecycleError(
                f"taskkill failed for PID {pid}: {result.stderr.strip()}"
            )
    else:
        try:
            os.killpg(pid, signal.SIGTERM)
        except ProcessLookupError:
            return warnings
        deadline = time.monotonic() + 3
        while time.monotonic() < deadline and _pid_running(pid):
            time.sleep(0.1)
        if _pid_running(pid):
            os.killpg(pid, signal.SIGKILL)
            warnings.append(f"gateway PID {pid} required SIGKILL")
    return warnings


def _close_browser(session_name: str) -> list[str]:
    warnings: list[str] = []
    executable = shutil.which("playwright-cli")
    if not executable:
        return ["playwright-cli not found; no named browser session was closed"]
    for action in ("close", "delete-data"):
        result = subprocess.run(
            [executable, f"-s={session_name}", action],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        if result.returncode:
            detail = (result.stderr or result.stdout).strip().splitlines()
            suffix = f": {detail[-1]}" if detail else ""
            warnings.append(f"playwright {action} returned {result.returncode}{suffix}")
    return warnings


def _copy_logs(runtime: Path, evidence: Path) -> list[str]:
    copied: list[str] = []
    evidence.mkdir(parents=True, exist_ok=True)
    for name in ("gateway.stdout.log", "gateway.stderr.log"):
        source = runtime / name
        if source.is_file():
            destination = evidence / name
            shutil.copy2(source, destination)
            copied.append(str(destination))
    return copied


def _wait_until_stopped(pid: int, ports: list[int], timeout: float = 5) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if not _pid_running(pid) and not any(_port_in_use(port) for port in ports):
            return
        time.sleep(0.1)
    active = [port for port in ports if _port_in_use(port)]
    raise LifecycleError(
        f"gateway cleanup incomplete: pid_running={_pid_running(pid)}, ports={active}"
    )


def _cleanup(
    manifest_path: Path, manifest: dict[str, Any], close_browser: bool
) -> dict[str, Any]:
    runtime = _validated_runtime(str(manifest["runtime_dir"]))
    evidence = Path(manifest["evidence_dir"]).resolve()
    pid = int(manifest["gateway_pid"])
    config_path = runtime / "config.json"
    ports = [int(manifest["websocket_port"]), int(manifest["gateway_port"])]
    warnings: list[str] = []

    if close_browser:
        warnings.extend(_close_browser(str(manifest["session_name"])))
    warnings.extend(_terminate_tree(pid, config_path))
    _wait_until_stopped(pid, ports)
    copied_logs = _copy_logs(runtime, evidence)
    if runtime.exists():
        shutil.rmtree(runtime)

    manifest.update(
        {
            "status": "cleaned",
            "cleaned_at": _now(),
            "runtime_removed": not runtime.exists(),
            "ports_released": not any(_port_in_use(port) for port in ports),
            "evidence_logs": copied_logs,
            "cleanup_warnings": warnings,
        }
    )
    _atomic_json(manifest_path, manifest)
    return {
        "ok": True,
        "status": manifest["status"],
        "manifest": str(manifest_path),
        "runtime_removed": manifest["runtime_removed"],
        "ports_released": manifest["ports_released"],
        "warnings": warnings,
    }


def _start(args: argparse.Namespace) -> dict[str, Any]:
    repo = _validated_repo(args.repo)
    evidence = _validated_evidence(repo, args.evidence_dir)
    run_id = _validated_run_id(args.run_id)
    runtime = _validated_runtime(str(RUNTIME_ROOT / run_id))
    manifest_path = evidence / MANIFEST_NAME
    if runtime.exists():
        raise LifecycleError(f"runtime directory already exists: {runtime}")
    if manifest_path.exists():
        raise LifecycleError(f"manifest already exists: {manifest_path}")

    websocket_port = _free_port()
    gateway_port = _free_port()
    while gateway_port == websocket_port:
        gateway_port = _free_port()

    workspace = runtime / "workspace"
    workspace.mkdir(parents=True)
    evidence.mkdir(parents=True, exist_ok=True)
    config_path = runtime / "config.json"
    stdout_path = runtime / "gateway.stdout.log"
    stderr_path = runtime / "gateway.stderr.log"
    config = {
        "agents": {
            "defaults": {
                "provider": "custom",
                "model": "verify-model",
                "workspace": str(workspace),
                "maxToolIterations": 1,
            }
        },
        "providers": {
            "custom": {
                "apiKey": "verify-no-external-call",
                "apiBase": "http://127.0.0.1:9/v1",
            }
        },
        "channels": {
            "websocket": {
                "enabled": True,
                "host": "127.0.0.1",
                "port": websocket_port,
            }
        },
        "gateway": {
            "host": "127.0.0.1",
            "port": gateway_port,
            "heartbeat": {"enabled": False},
        },
    }
    config_path.write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    command = [sys.executable, "-m", "nanobot", "gateway", "--config", str(config_path)]
    popen_kwargs: dict[str, Any] = {"cwd": repo}
    if os.name == "nt":
        popen_kwargs["creationflags"] = (
            subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW
        )
    else:
        popen_kwargs["start_new_session"] = True
    with (
        stdout_path.open("wb") as stdout_handle,
        stderr_path.open("wb") as stderr_handle,
    ):
        process = subprocess.Popen(
            command,
            stdout=stdout_handle,
            stderr=stderr_handle,
            **popen_kwargs,
        )

    bootstrap_url = f"http://127.0.0.1:{websocket_port}/webui/bootstrap"
    manifest: dict[str, Any] = {
        "schema_version": 1,
        "status": "starting",
        "created_at": _now(),
        "run_id": run_id,
        "repo": str(repo),
        "runtime_dir": str(runtime),
        "evidence_dir": str(evidence),
        "gateway_pid": process.pid,
        "websocket_port": websocket_port,
        "gateway_port": gateway_port,
        "url": f"http://127.0.0.1:{websocket_port}/",
        "bootstrap_url": bootstrap_url,
        "session_name": f"nanobot-webui-{run_id}",
    }
    _atomic_json(manifest_path, manifest)

    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    deadline = time.monotonic() + args.timeout
    last_error = "not ready"
    while time.monotonic() < deadline:
        if process.poll() is not None:
            last_error = f"gateway exited with code {process.returncode}"
            break
        try:
            with opener.open(bootstrap_url, timeout=2) as response:
                if response.status == 200:
                    manifest.update({"status": "ready", "ready_at": _now()})
                    _atomic_json(manifest_path, manifest)
                    return {
                        "ok": True,
                        "status": "ready",
                        "manifest": str(manifest_path),
                        "gateway_pid": process.pid,
                        "url": manifest["url"],
                        "session_name": manifest["session_name"],
                    }
                last_error = f"HTTP {response.status}"
        except (OSError, urllib.error.URLError) as exc:
            last_error = str(exc)
        time.sleep(0.25)

    manifest.update(
        {"status": "start_failed", "failure": last_error, "failed_at": _now()}
    )
    _atomic_json(manifest_path, manifest)
    cleanup_result = _cleanup(manifest_path, manifest, close_browser=False)
    cleanup_result.update({"ok": False, "status": "start_failed", "error": last_error})
    return cleanup_result


def _status(args: argparse.Namespace) -> dict[str, Any]:
    manifest_path = Path(args.manifest).resolve()
    manifest = _load_manifest(manifest_path)
    runtime = _validated_runtime(str(manifest["runtime_dir"]))
    pid = int(manifest["gateway_pid"])
    running = _pid_running(pid)
    matching = _process_matches(pid, runtime / "config.json") if running else False
    websocket_open = _port_in_use(int(manifest["websocket_port"]))
    gateway_open = _port_in_use(int(manifest["gateway_port"]))
    return {
        "ok": True,
        "manifest_status": manifest["status"],
        "gateway_pid": pid,
        "process_running": running,
        "process_matches_manifest": matching,
        "websocket_port_in_use": websocket_open,
        "gateway_port_in_use": gateway_open,
        "runtime_exists": runtime.exists(),
        "url": manifest["url"],
        "session_name": manifest["session_name"],
    }


def _cleanup_command(args: argparse.Namespace) -> dict[str, Any]:
    manifest_path = Path(args.manifest).resolve()
    manifest = _load_manifest(manifest_path)
    if manifest.get("status") == "cleaned":
        runtime = _validated_runtime(str(manifest["runtime_dir"]))
        ports = [int(manifest["websocket_port"]), int(manifest["gateway_port"])]
        return {
            "ok": True,
            "status": "cleaned",
            "manifest": str(manifest_path),
            "runtime_removed": not runtime.exists(),
            "ports_released": not any(_port_in_use(port) for port in ports),
            "warnings": manifest.get("cleanup_warnings", []),
        }
    return _cleanup(manifest_path, manifest, close_browser=True)


def _purge_evidence(args: argparse.Namespace) -> dict[str, Any]:
    manifest_path = Path(args.manifest).resolve()
    manifest = _load_manifest(manifest_path)
    if manifest.get("status") != "cleaned":
        raise LifecycleError("cleanup must succeed before evidence can be purged")
    repo = _validated_repo(str(manifest["repo"]))
    evidence = _validated_evidence(repo, str(manifest["evidence_dir"]))
    if manifest_path.parent != evidence:
        raise LifecycleError(
            "manifest is not stored directly inside its evidence directory"
        )
    shutil.rmtree(evidence)
    return {"ok": True, "status": "evidence_purged", "evidence_dir": str(evidence)}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    start = commands.add_parser(
        "start", help="start an isolated gateway and wait for readiness"
    )
    start.add_argument("--repo", required=True, help="nanobot repository root")
    start.add_argument(
        "--evidence-dir", required=True, help="repo-local .verify-evidence-* directory"
    )
    start.add_argument("--run-id", help="optional stable identifier for this run")
    start.add_argument(
        "--timeout", type=float, default=30, help="readiness timeout in seconds"
    )
    start.set_defaults(handler=_start)

    status = commands.add_parser(
        "status", help="report process, port, and runtime state"
    )
    status.add_argument("--manifest", required=True)
    status.set_defaults(handler=_status)

    cleanup = commands.add_parser(
        "cleanup", help="close browser, stop gateway, and delete runtime"
    )
    cleanup.add_argument("--manifest", required=True)
    cleanup.set_defaults(handler=_cleanup_command)

    purge = commands.add_parser(
        "purge-evidence",
        help="delete an already-cleaned evidence directory after user approval",
    )
    purge.add_argument("--manifest", required=True)
    purge.set_defaults(handler=_purge_evidence)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        result = args.handler(args)
    except (LifecycleError, OSError, subprocess.SubprocessError) as exc:
        _emit({"ok": False, "error": str(exc), "command": args.command})
        return 1
    _emit(result)
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
