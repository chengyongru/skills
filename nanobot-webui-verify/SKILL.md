---
name: nanobot-webui-verify
description: Primary black-box verifier for nanobot WebUI, gateway, websocket, routing, settings, chat, sidebar, refresh persistence, and Playwright flows. Use for $verify and PR-readiness requests involving browser-visible nanobot behavior.
---

# Nanobot WebUI Verify

Verify the built WebUI through the real gateway and a headless browser.

1. Inspect the diff and select the changed user flow plus its highest-risk edge.
2. Run focused WebUI tests and `bun run build` from `webui`.
3. Start an isolated gateway from the repository root:

```powershell
$root = (Get-Location).Path
$helper = "<skill>\scripts\webui_runtime.py"
$runId = "{0}-{1}" -f $PID, ([guid]::NewGuid().ToString('N').Substring(0, 8))
$evidenceDir = Join-Path $root "webui\.verify-evidence-$runId"
$started = python $helper start --repo $root --evidence-dir $evidenceDir --run-id $runId | ConvertFrom-Json
```

4. Use `$started.url` and `$started.session_name` with `playwright-cli`. Set `NO_PROXY/no_proxy` for localhost when proxy variables are active. Assert visible state, the changed interaction, console/runtime health, and refresh/persistence when relevant. Use a temporary Playwright spec only for assertions that are awkward in the CLI.
5. For persisted chat replay, use a deterministic built-in command such as `/model` and prove replay through `GET /api/sessions/<encoded-key>/webui-thread`. Seed isolated JSONL as UTF-8 with no BOM when legacy backfill is the target.
6. Always finish with:

```powershell
python $helper cleanup --manifest $started.manifest
```

Cleanup passes when `runtime_removed` and `ports_released` are true. Use `status` for ownership conflicts. Preserve evidence, report its path, and run `purge-evidence` after the user approves deletion.

Return exact actions, evidence, PASS/WARN/FAIL, and limitations directly in the conversation.
