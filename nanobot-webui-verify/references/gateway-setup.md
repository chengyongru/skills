# Gateway Setup Reference

Use a repo-local temporary directory with a unique suffix so multiple black-box verifications can run at the same time. Keep workspace, config, logs, and PID inside that directory.

```powershell
$root = (Get-Location).Path
$runId = "{0}-{1}" -f $PID, ([guid]::NewGuid().ToString('N').Substring(0, 8))
$verifyDir = Join-Path $root ".verify-webui-$runId"
$configPath = Join-Path $verifyDir 'config.json'
$workspacePath = Join-Path $verifyDir 'workspace'
New-Item -ItemType Directory -Force -Path $verifyDir, $workspacePath | Out-Null

function Get-FreePort {
  $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, 0)
  $listener.Start()
  $port = $listener.LocalEndpoint.Port
  $listener.Stop()
  return $port
}
$websocketPort = Get-FreePort
$gatewayPort = Get-FreePort

$sourceConfig = Join-Path $HOME '.nanobot\config.json'
if (Test-Path $sourceConfig) {
  Copy-Item -LiteralPath $sourceConfig -Destination $configPath
  $config = Get-Content -Raw -Path $configPath | ConvertFrom-Json
} else {
  $config = [pscustomobject]@{}
}

if (-not $config.agents) { $config | Add-Member -NotePropertyName agents -NotePropertyValue ([pscustomobject]@{}) }
if (-not $config.agents.defaults) { $config.agents | Add-Member -NotePropertyName defaults -NotePropertyValue ([pscustomobject]@{}) }
if (-not $config.agents.defaults.provider) { $config.agents.defaults | Add-Member -Force -NotePropertyName provider -NotePropertyValue 'custom' }
if (-not $config.agents.defaults.model) { $config.agents.defaults | Add-Member -Force -NotePropertyName model -NotePropertyValue 'verify-model' }
$config.agents.defaults | Add-Member -Force -NotePropertyName workspace -NotePropertyValue $workspacePath
$config.agents.defaults | Add-Member -Force -NotePropertyName maxToolIterations -NotePropertyValue 1

if (-not $config.providers) { $config | Add-Member -NotePropertyName providers -NotePropertyValue ([pscustomobject]@{}) }
if (-not $config.providers.custom) {
  $config.providers | Add-Member -NotePropertyName custom -NotePropertyValue ([pscustomobject]@{
    apiKey = 'verify-no-external-call'
    apiBase = 'http://127.0.0.1:9/v1'
  })
}

if (-not $config.channels) { $config | Add-Member -NotePropertyName channels -NotePropertyValue ([pscustomobject]@{}) }
$config.channels | Add-Member -Force -NotePropertyName websocket -NotePropertyValue ([pscustomobject]@{
  enabled = $true
  host = '127.0.0.1'
  port = $websocketPort
})

$config | Add-Member -Force -NotePropertyName gateway -NotePropertyValue ([pscustomobject]@{
  host = '127.0.0.1'
  port = $gatewayPort
  heartbeat = [pscustomobject]@{ enabled = $false }
})
$config | ConvertTo-Json -Depth 8 | Set-Content -Path $configPath -Encoding UTF8

$out = Join-Path $verifyDir 'gateway.out.log'
$err = Join-Path $verifyDir 'gateway.err.log'
Remove-Item -Force -ErrorAction SilentlyContinue $out, $err
$p = Start-Process -FilePath python -ArgumentList @('-m','nanobot','gateway','--config',$configPath) -WorkingDirectory $root -RedirectStandardOutput $out -RedirectStandardError $err -PassThru -WindowStyle Hidden
$p.Id | Set-Content (Join-Path $verifyDir 'gateway.pid')
```

Wait until `$websocketPort` accepts TCP connections before launching Playwright. If the browser URL is needed in a later command, write `$websocketPort` to a file in `$verifyDir` or keep the same PowerShell session.
