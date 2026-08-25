[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateNotNullOrEmpty()]
    [string]$Name,

    [Parameter(Mandatory)]
    [ValidateNotNullOrEmpty()]
    [string]$Task,

    [ValidateSet("tab", "pane")]
    [string]$Placement = "tab",

    [ValidateSet("right", "down")]
    [string]$Direction,

    [ValidateNotNullOrEmpty()]
    [string]$Cwd = (Get-Location).Path,

    [string]$Label,

    [ValidateRange(5000, 120000)]
    [int]$StartupTimeoutMs = 30000,

    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Invoke-HerdrJson {
    param([Parameter(Mandatory)][string[]]$Arguments)

    $output = @(& herdr @Arguments 2>&1 | ForEach-Object { "$_" })
    if ($LASTEXITCODE -ne 0) {
        throw "herdr $($Arguments -join ' ') failed: $($output -join [Environment]::NewLine)"
    }

    $json = $output | Where-Object { $_.TrimStart().StartsWith("{") } | Select-Object -Last 1
    if (-not $json) {
        throw "herdr $($Arguments -join ' ') returned no JSON response"
    }

    try {
        return $json | ConvertFrom-Json
    }
    catch {
        throw "Could not parse Herdr response for '$($Arguments -join ' ')': $json"
    }
}

function Invoke-HerdrCommand {
    param([Parameter(Mandatory)][string[]]$Arguments)

    $output = @(& herdr @Arguments 2>&1 | ForEach-Object { "$_" })
    if ($LASTEXITCODE -ne 0) {
        throw "herdr $($Arguments -join ' ') failed: $($output -join [Environment]::NewLine)"
    }
}

function Get-DetectedAgent {
    param([Parameter(Mandatory)][string]$PaneId)

    $output = @(& herdr agent get $PaneId 2>$null | ForEach-Object { "$_" })
    if ($LASTEXITCODE -ne 0) {
        return $null
    }

    $json = $output | Where-Object { $_.TrimStart().StartsWith("{") } | Select-Object -Last 1
    if (-not $json) {
        return $null
    }

    return $json | ConvertFrom-Json
}

function New-UniqueAgentName {
    param([Parameter(Mandatory)][string]$BaseName)

    $slug = $BaseName.ToLowerInvariant() -replace "[^a-z0-9_-]", "-"
    $slug = $slug.Trim([char[]]"-_")
    if (-not $slug) {
        $slug = "scode"
    }
    if ($slug[0] -notmatch "[a-z]") {
        $slug = "scode-$slug"
    }
    if ($slug.Length -gt 25) {
        $slug = $slug.Substring(0, 25).TrimEnd([char[]]"-_")
    }

    $suffix = [guid]::NewGuid().ToString("N").Substring(0, 6)
    return "$slug-$suffix"
}

if ($env:HERDR_ENV -ne "1") {
    throw "This helper must run inside a Herdr-managed pane (HERDR_ENV=1)."
}

if (-not (Get-Command herdr -ErrorAction SilentlyContinue)) {
    throw "The herdr command is not available."
}
if (-not (Get-Command scode -ErrorAction SilentlyContinue)) {
    throw "The scode PowerShell launcher is not available in this shell."
}

$resolvedCwd = (Resolve-Path -LiteralPath $Cwd).Path
if (-not (Test-Path -LiteralPath $resolvedCwd -PathType Container)) {
    throw "Delegation cwd is not a directory: $resolvedCwd"
}

$current = Invoke-HerdrJson -Arguments @("pane", "current", "--current")
$currentPane = $current.result.pane
$workspaceId = $currentPane.workspace_id
$agentName = New-UniqueAgentName -BaseName $Name
if ([string]::IsNullOrWhiteSpace($Label)) {
    $Label = $Name
}

if ($Placement -eq "pane" -and -not $Direction) {
    $layout = Invoke-HerdrJson -Arguments @(
        "pane", "layout", "--pane", $currentPane.pane_id
    )
    $rect = $layout.result.layout.panes |
        Where-Object { $_.pane_id -eq $currentPane.pane_id } |
        Select-Object -First 1
    if ($rect -and $rect.rect.width -ge 100 -and $rect.rect.width -ge (2 * $rect.rect.height)) {
        $Direction = "right"
    }
    else {
        $Direction = "down"
    }
}

if ($DryRun) {
    [pscustomobject]@{
        status               = "dry-run"
        placement            = $Placement
        direction            = $Direction
        workspace_id         = $workspaceId
        source_pane_id       = $currentPane.pane_id
        cwd                  = $resolvedCwd
        label                = $Label
        agent_name           = $agentName
        launcher             = "scode"
        waits_for_completion = $false
    } | ConvertTo-Json -Compress
    exit 0
}

if ($Placement -eq "tab") {
    $created = Invoke-HerdrJson -Arguments @(
        "tab", "create", "--workspace", $workspaceId, "--cwd", $resolvedCwd,
        "--label", $Label, "--no-focus"
    )
    $tabId = $created.result.tab.tab_id
    $paneId = $created.result.root_pane.pane_id
}
else {
    $created = Invoke-HerdrJson -Arguments @(
        "pane", "split", "--pane", $currentPane.pane_id, "--direction", $Direction,
        "--cwd", $resolvedCwd, "--no-focus"
    )
    $paneId = $created.result.pane.pane_id
    $tabId = $created.result.pane.tab_id
}

Invoke-HerdrCommand -Arguments @("pane", "run", $paneId, "scode")

$stopwatch = [Diagnostics.Stopwatch]::StartNew()
$detected = $null
while ($stopwatch.ElapsedMilliseconds -lt $StartupTimeoutMs) {
    $detected = Get-DetectedAgent -PaneId $paneId
    if ($detected) {
        $agentStatus = $detected.result.agent.agent_status
        if ($agentStatus -in @("idle", "done")) {
            break
        }
        if ($agentStatus -eq "blocked") {
            throw "scode started in $paneId but is blocked before task submission."
        }
    }
    Start-Sleep -Milliseconds 250
}

if (-not $detected -or $detected.result.agent.agent_status -notin @("idle", "done")) {
    throw "Timed out waiting for Herdr to detect an idle scode agent in $paneId. The target was left open for inspection."
}

Invoke-HerdrJson -Arguments @("agent", "rename", $paneId, $agentName) | Out-Null
Invoke-HerdrJson -Arguments @("agent", "prompt", $agentName, $Task) | Out-Null

[pscustomobject]@{
    status               = "delegated"
    placement            = $Placement
    direction            = $Direction
    workspace_id         = $workspaceId
    tab_id               = $tabId
    pane_id              = $paneId
    cwd                  = $resolvedCwd
    label                = $Label
    agent_name           = $agentName
    launcher             = "scode"
    waits_for_completion = $false
} | ConvertTo-Json -Compress
