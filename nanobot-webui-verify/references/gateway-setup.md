# Gateway Setup Reference

Use the bundled lifecycle helper. It replaces ad hoc PowerShell for port allocation, config generation, process startup, readiness polling, PID tracking, log collection, and recursive runtime cleanup.

## Start

```powershell
$root = (Get-Location).Path
$runId = "{0}-{1}" -f $PID, ([guid]::NewGuid().ToString('N').Substring(0, 8))
$evidenceDir = Join-Path $root "webui\.verify-evidence-$runId"
$helper = "C:\Users\HR\skills\nanobot-webui-verify\scripts\webui_runtime.py"
$started = python $helper start --repo $root --evidence-dir $evidenceDir --run-id $runId |
  ConvertFrom-Json
if (-not $started.ok) { throw $started.error }
```

Successful output contains only the values needed by later commands:

```json
{"ok":true,"status":"ready","manifest":"...runtime-manifest.json","gateway_pid":1234,"url":"http://127.0.0.1:54321/","session_name":"nanobot-webui-..."}
```

The helper:

- creates the runtime only under `%TEMP%\nanobot-webui-verify\<run-id>`;
- creates a minimal config with a non-routable dummy provider, isolated workspace, disabled heartbeat, and fresh websocket/gateway ports;
- writes JSON as UTF-8 with no BOM;
- launches the real gateway as a hidden child process and records its actual PID;
- bypasses proxies and waits for `GET /webui/bootstrap` to return HTTP 200;
- removes failed-start runtimes after preserving their logs.

The minimal config leaves the user's `~/.nanobot/config.json` untouched and keeps real provider secrets and external model calls outside the verification run.

## Status

```powershell
python $helper status --manifest $started.manifest
```

Status reports whether the PID is alive, whether its command line still matches the exact manifest config, whether both ports are owned, and whether the runtime directory exists. Port checks use local bind ownership checks that send zero traffic to the server.

## Cleanup

```powershell
python $helper cleanup --manifest $started.manifest
```

Cleanup is idempotent. It:

1. closes and deletes the named `playwright-cli` session when available;
2. matches the live PID command line to the exact config path before stopping it;
3. stops the matching process tree, then verifies the PID and both ports are gone;
4. copies gateway stdout/stderr into the evidence directory;
5. validates that the runtime is below the fixed temp root and deletes it recursively;
6. updates the retained manifest with `runtime_removed`, `ports_released`, logs, and warnings.

Use this command as the complete lifecycle cleanup path; it replaces per-file cleanup and shell/process-name heuristics.

## Evidence Deletion

Evidence remains after normal cleanup. Only after explicit user approval, delete the exact evidence directory through the manifest:

```powershell
python $helper purge-evidence --manifest $started.manifest
```

The helper requires a successfully cleaned manifest stored directly in a `.verify-evidence-*` directory below the repository's `webui` directory.

## Seeded JSONL

If a verification seeds session or transcript JSONL files directly, write them as UTF-8 with no BOM and store them in the isolated workspace path while the gateway is active. Use `[System.IO.File]` with `UTF8Encoding($false)` on Windows for deterministic encoding.

## Failure Recovery

- If `start` returns `ok: false`, inspect `gateway.stdout.log`, `gateway.stderr.log`, and `runtime-manifest.json` in the evidence directory. The process and runtime have already been cleaned.
- If `cleanup` reports a PID mismatch, run `status`, leave that process untouched, inspect its ownership, and report the conflict.
- If cleanup reports a port still owned, retain the evidence, run `status`, and report WARN or BLOCKED with the exact PID/ports.
