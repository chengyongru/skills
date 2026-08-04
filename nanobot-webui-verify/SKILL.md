---
name: nanobot-webui-verify
description: Verify nanobot WebUI changes from a user perspective. Use as the primary verification workflow for nanobot WebUI routing, settings, chat, sidebar, gateway, websocket, refresh persistence, Playwright, headless-browser, and other browser-visible checks, including $verify requests and PR readiness checks involving these surfaces.
---

# Nanobot WebUI Verify

## Overview

Verify nanobot WebUI changes through the built frontend served by the real gateway, then exercise user-visible behavior with headless Playwright. Prefer `playwright-cli` for concise black-box browser checks; fall back to Playwright test specs when assertions require more structure. Treat unit tests and build as prerequisites, but rely on browser evidence for refresh, routing, websocket, and layout behavior.

## Workflow

1. Inspect the diff and identify the user-facing flows to verify.
2. Run focused WebUI tests first:

```powershell
cd webui
bun run test -- <relevant-test-file>
```

3. Build the WebUI:

```powershell
cd webui
bun run build
```

4. Use the bundled lifecycle helper from the repository root. It creates a minimal isolated config under the fixed system-temp root, records the real gateway PID and ports, waits for `/webui/bootstrap`, and emits one compact JSON result:

```powershell
$root = (Get-Location).Path
$runId = "{0}-{1}" -f $PID, ([guid]::NewGuid().ToString('N').Substring(0, 8))
$evidenceDir = Join-Path $root "webui\.verify-evidence-$runId"
$helper = "C:\Users\HR\skills\nanobot-webui-verify\scripts\webui_runtime.py"
$started = python $helper start --repo $root --evidence-dir $evidenceDir --run-id $runId |
  ConvertFrom-Json
if (-not $started.ok) { throw $started.error }
$manifest = $started.manifest
$session = $started.session_name
$webuiUrl = $started.url
```

5. Run `playwright-cli` headless checks against `$webuiUrl` using `$session`.

6. Always run the helper cleanup, even after a failed browser assertion. It closes the named browser session, validates and stops the exact gateway process tree, verifies both ports are released, copies gateway logs into the evidence directory, and deletes the runtime directory in one command:

```powershell
python $helper cleanup --manifest $manifest
```

7. Run `status` if cleanup or process ownership is uncertain:

```powershell
python $helper status --manifest $manifest
```

8. Report exact commands, pass/fail status, evidence paths, and any warnings that matter.

## Lifecycle Pattern

- Route gateway startup, status, and cleanup through `scripts/webui_runtime.py`.
- Confirm shutdown with the actual child PID and port state recorded by the helper.
- Keep runtime state under the helper's fixed system-temp root and remove it with one `cleanup` command.
- Stop a gateway process tree only after the manifest's exact config matches its command line.
- Use `/webui/bootstrap` for readiness and the helper's non-traffic port ownership checks for cleanup.
- Keep screenshots and snapshots in the repo-local `.verify-evidence-*` directory and stage source paths explicitly.
- After the user approves deletion of retained evidence, remove the exact directory through the helper:

```powershell
python $helper purge-evidence --manifest $manifest
```

For the command contract, manifest fields, and failure recovery, read [references/gateway-setup.md](references/gateway-setup.md).

## Proxy Rules

When GitHub or network commands need a proxy, keep those settings scoped to that command. For localhost browser verification, bypass proxies:

```powershell
$env:NO_PROXY='127.0.0.1,localhost'
$env:no_proxy='127.0.0.1,localhost'
$env:ALL_PROXY=''
$env:all_proxy=''
```

## Playwright CLI Pattern

Use `playwright-cli` first for black-box checks. It is headless by default, supports named sessions with `-s=`, and can inspect, click, reload, evaluate page state, and capture screenshots from simple CLI commands.

Install only when missing:

```powershell
npm install -g @playwright/cli@latest
playwright-cli --help
```

The lifecycle helper returns a unique session name and URL:

```powershell
playwright-cli -s=$session open "$($webuiUrl.TrimEnd('/'))/#/settings?section=models"
$snapshotPath = Join-Path $evidenceDir 'settings-models.yaml'
playwright-cli -s=$session snapshot --filename $snapshotPath
if (-not (Test-Path $snapshotPath)) { throw "snapshot was not created: $snapshotPath" }
playwright-cli -s=$session eval "() => ({ hash: window.location.hash, text: document.body.innerText })"
playwright-cli -s=$session reload
playwright-cli -s=$session eval "() => ({ hash: window.location.hash, text: document.body.innerText })"
$screenshotPath = Join-Path $evidenceDir 'after-reload.png'
playwright-cli -s=$session screenshot --filename $screenshotPath
if (-not (Test-Path $screenshotPath)) { throw "screenshot was not created: $screenshotPath" }
```

For route-persistence checks, verify both:

- The expected UI text is visible in the snapshot or `document.body.innerText`.
- `window.location.hash` still matches the expected route after `reload`.

When verifying persisted chat refresh specifically:

- Prefer a built-in command such as `/model` for a deterministic assistant response using only local gateway behavior.
- Prove replay through the public `GET /api/sessions/<encoded-key>/webui-thread` route using the bootstrap API token. Use transcript helpers only for diagnosis.
- For legacy transcript backfill, seed isolated `workspace/sessions/*.jsonl` and `webui/*.jsonl` files as UTF-8 with no BOM, then fetch the public route.
- For transcript append failure behavior, make only the target transcript JSONL path a directory to trigger an append `OSError` for that chat while preserving the rest of the runtime tree.

The helper closes and deletes the named browser session during cleanup.

## Playwright Test Fallback

Use this only when `playwright-cli` is too awkward for the needed assertions, polling, or multi-step logic. Read [references/playwright-test-fallback.md](references/playwright-test-fallback.md) for the temporary spec pattern.

## Cleanup

Cleanup is complete when the helper reports `runtime_removed: true` and `ports_released: true`. Preserve screenshots and snapshots in `$evidenceDir`, report the path, then ask: "是否删除保留的验证截图/快照目录 `$evidenceDir`？" Run `purge-evidence` after explicit confirmation.

Before committing, check `git status --short`, restore generated files such as `webui/bun.lock` when verification tooling alone changed them, and stage intended source paths explicitly so `.verify-evidence-*` stays outside the commit.
