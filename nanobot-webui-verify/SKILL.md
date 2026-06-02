---
name: nanobot-webui-verify
description: Verify nanobot WebUI changes from a user perspective. Use when working in the nanobot repository after WebUI routing, settings, chat, sidebar, or gateway-facing changes; when the user mentions validating nanobot WebUI with $verify, Playwright, headless browser, gateway, websocket port, refresh persistence, or black-box UI checks; or when a PR needs evidence that the built WebUI works through the real gateway.
---

# Nanobot WebUI Verify

## Overview

Verify nanobot WebUI changes through the built frontend served by the real gateway, then exercise user-visible behavior with headless Playwright. Prefer `playwright-cli` for concise black-box browser checks; fall back to Playwright test specs when assertions require more structure. Treat unit tests and build as prerequisites, but rely on browser evidence for refresh, routing, websocket, and layout behavior.

## Workflow

1. Inspect the diff and identify the user-facing flows to verify.
2. Run focused WebUI tests first:

```powershell
cd webui
npm run test -- <relevant-test-file>
```

3. Build the WebUI:

```powershell
cd webui
npm run build
```

4. Start `nanobot gateway` from the repository root with a per-run temporary config copied from `~/.nanobot` when available. Assign fresh free ports for `channels.websocket.port` and `gateway.port`; access the browser through the websocket port.

5. Run `playwright-cli` headless checks against `http://127.0.0.1:<websocket-port>/`. Use a unique session name per verification run.

6. Stop the gateway, close the `playwright-cli` session, and remove temporary specs, logs, test-results, and config directories.

7. Report exact commands, pass/fail status, and any warnings that matter.

## Gateway Setup

For concrete PowerShell setup, read [references/gateway-setup.md](references/gateway-setup.md). The important constraints are:

- Use a unique `.verify-webui-<runId>` directory per verification run.
- Copy `~/.nanobot/config.json` into that directory when it exists, then mutate the copy only.
- Assign fresh free `channels.websocket.port` and `gateway.port` values per gateway.
- Use different websocket and gateway ports, and open the browser through the websocket port.

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

Use a session name tied to `$runId` so concurrent verifications do not share browser state:

```powershell
$session = "nanobot-webui-$runId"
$env:NANOBOT_WEBUI_URL = "http://127.0.0.1:$websocketPort"

playwright-cli -s=$session open "$env:NANOBOT_WEBUI_URL/#/settings?section=models"
playwright-cli -s=$session snapshot --filename=(Join-Path $verifyDir 'settings-models.yaml')
playwright-cli -s=$session eval "() => ({ hash: window.location.hash, text: document.body.innerText })"
playwright-cli -s=$session reload
playwright-cli -s=$session eval "() => ({ hash: window.location.hash, text: document.body.innerText })"
playwright-cli -s=$session screenshot --filename=(Join-Path $verifyDir 'after-reload.png')
```

For route-persistence checks, verify both:

- The expected UI text is visible in the snapshot or `document.body.innerText`.
- `window.location.hash` still matches the expected route after `reload`.

Close the named browser session during cleanup:

```powershell
playwright-cli -s=$session close
playwright-cli -s=$session delete-data
```

## Playwright Test Fallback

Use this only when `playwright-cli` is too awkward for the needed assertions, polling, or multi-step logic. Read [references/playwright-test-fallback.md](references/playwright-test-fallback.md) for the temporary spec pattern.

## Cleanup

Always stop the gateway process before finishing:

```powershell
if ($session) {
  playwright-cli -s=$session close
  playwright-cli -s=$session delete-data
}
if (Test-Path (Join-Path $verifyDir 'gateway.pid')) {
  $pidText = (Get-Content (Join-Path $verifyDir 'gateway.pid') -Raw).Trim()
  if ($pidText) {
    Stop-Process -Id ([int]$pidText) -Force -ErrorAction SilentlyContinue
  }
}
Remove-Item -Force -ErrorAction SilentlyContinue (Join-Path $root "webui\.verify-webui-$runId.spec.mjs")
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue (Join-Path $root 'webui\test-results')
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $verifyDir
```

Before committing, check `git status --short` and restore accidental generated files such as `webui/bun.lock` if they were only touched by verification tooling.
