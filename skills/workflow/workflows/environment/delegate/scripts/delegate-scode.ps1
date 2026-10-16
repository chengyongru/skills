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

    [ValidateRange(1000, 30000)]
    [int]$SubmissionTimeoutMs = 10000,

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

function Invoke-HerdrCapture {
    param([Parameter(Mandatory)][string[]]$Arguments)

    $output = @(& herdr @Arguments 2>&1 | ForEach-Object { "$_" })
    return [pscustomobject]@{
        ExitCode = $LASTEXITCODE
        Output   = $output
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

function Test-AgentSubmission {
    param(
        [Parameter(Mandatory)]$Detected,
        [Parameter(Mandatory)][long]$BaselineStateChangeSeq
    )

    $agent = $Detected.result.agent
    if ($agent.agent_status -in @("working", "blocked")) {
        return $true
    }

    return (
        [long]$agent.state_change_seq -gt $BaselineStateChangeSeq -and
        $agent.agent_status -in @("idle", "done")
    )
}

function Wait-AgentSubmission {
    param(
        [Parameter(Mandatory)][string]$AgentName,
        [Parameter(Mandatory)][long]$BaselineStateChangeSeq,
        [Parameter(Mandatory)][int]$TimeoutMs
    )

    $stopwatch = [Diagnostics.Stopwatch]::StartNew()
    while ($stopwatch.ElapsedMilliseconds -lt $TimeoutMs) {
        $detected = Get-DetectedAgent -PaneId $AgentName
        if ($detected -and (Test-AgentSubmission `
                -Detected $detected `
                -BaselineStateChangeSeq $BaselineStateChangeSeq)) {
            return $detected
        }
        Start-Sleep -Milliseconds 100
    }

    return $null
}

function Get-AgentDetectionText {
    param([Parameter(Mandatory)][string]$AgentName)

    $read = Invoke-HerdrCapture -Arguments @(
        "agent", "read", $AgentName, "--source", "detection", "--lines", "120"
    )
    if ($read.ExitCode -ne 0) {
        throw "Could not inspect the active scode composer in ${AgentName}: $($read.Output -join [Environment]::NewLine)"
    }

    return $read.Output -join [Environment]::NewLine
}

function Test-TaskInActiveComposer {
    param(
        [Parameter(Mandatory)][string]$DetectionText,
        [Parameter(Mandatory)][string]$Task
    )

    $lines = $DetectionText -split "`r?`n"
    $composerStart = -1
    for ($index = 0; $index -lt $lines.Count; $index++) {
        if ($lines[$index] -match "^\s*›\s*") {
            $composerStart = $index
        }
    }
    if ($composerStart -lt 0) {
        return $false
    }

    $taskProbe = $Task -replace "\s", ""
    if ($taskProbe.Length -gt 64) {
        $taskProbe = $taskProbe.Substring(0, 64)
    }
    $activeComposer = ($lines[$composerStart..($lines.Count - 1)] -join "") -replace "\s", ""
    if ($activeComposer.StartsWith("›AskCodextodoanything")) {
        return $false
    }
    return $taskProbe.Length -gt 0 -and $activeComposer.Contains($taskProbe)
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
        status                = "dry-run"
        placement             = $Placement
        direction             = $Direction
        workspace_id          = $workspaceId
        source_pane_id        = $currentPane.pane_id
        cwd                   = $resolvedCwd
        label                 = $Label
        agent_name            = $agentName
        launcher              = "scode"
        submission_timeout_ms = $SubmissionTimeoutMs
        waits_for_completion  = $false
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

Invoke-HerdrCommand -Arguments @(
    "pane", "run", $paneId, "scode -c check_for_update_on_startup=false"
)

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
$ready = Get-DetectedAgent -PaneId $agentName
if (-not $ready -or $ready.result.agent.agent_status -notin @("idle", "done")) {
    throw "scode in $paneId stopped being ready before task submission. The target was left open for inspection; delegated was not returned."
}

$baselineStateChangeSeq = [long]$ready.result.agent.state_change_seq
$prompt = Invoke-HerdrCapture -Arguments @(
    "agent", "prompt", $agentName, $Task,
    "--wait", "--until", "working", "--timeout", "$SubmissionTimeoutMs"
)
$submission = $null
$confirmation = $null
$enterRetried = $false

if ($prompt.ExitCode -eq 0) {
    $submission = Get-DetectedAgent -PaneId $agentName
    $confirmation = "herdr-observed-working"
}
else {
    $submission = Get-DetectedAgent -PaneId $agentName
    if ($submission -and (Test-AgentSubmission `
            -Detected $submission `
            -BaselineStateChangeSeq $baselineStateChangeSeq)) {
        $confirmation = "lifecycle-changed-after-prompt"
    }
    elseif (($prompt.Output -join "`n") -notmatch "(?i)(agent_prompt_stalled|timeout)") {
        throw "Task submission failed in ${paneId}: $($prompt.Output -join [Environment]::NewLine). The target was left open for inspection; delegated was not returned."
    }
}

if (-not $confirmation) {
    $beforeRetry = Get-DetectedAgent -PaneId $agentName
    if ($beforeRetry -and (Test-AgentSubmission `
            -Detected $beforeRetry `
            -BaselineStateChangeSeq $baselineStateChangeSeq)) {
        $submission = $beforeRetry
        $confirmation = "lifecycle-changed-before-enter-retry"
    }
    elseif (
        $beforeRetry -and
        $beforeRetry.result.agent.agent_status -in @("idle", "done") -and
        (Test-TaskInActiveComposer `
            -DetectionText (Get-AgentDetectionText -AgentName $agentName) `
            -Task $Task)
    ) {
        Invoke-HerdrJson -Arguments @("agent", "send-keys", $agentName, "enter") | Out-Null
        $enterRetried = $true
        $submission = Wait-AgentSubmission `
            -AgentName $agentName `
            -BaselineStateChangeSeq $baselineStateChangeSeq `
            -TimeoutMs $SubmissionTimeoutMs
        if ($submission) {
            $confirmation = "lifecycle-changed-after-enter-retry"
        }
    }
}

if (-not $confirmation) {
    throw "Task submission could not be confirmed in $paneId within $SubmissionTimeoutMs ms. Enter was retried only when the task was still in the active composer. The target was left open for inspection; delegated was not returned."
}

$submissionStatus = if ($submission) {
    $submission.result.agent.agent_status
}
else {
    "working-observed"
}

[pscustomobject]@{
    status                  = "delegated"
    placement               = $Placement
    direction               = $Direction
    workspace_id            = $workspaceId
    tab_id                  = $tabId
    pane_id                 = $paneId
    cwd                     = $resolvedCwd
    label                   = $Label
    agent_name              = $agentName
    launcher                = "scode"
    submission_timeout_ms   = $SubmissionTimeoutMs
    submission_confirmed    = $true
    submission_confirmation = $confirmation
    submission_status       = $submissionStatus
    enter_retried           = $enterRetried
    waits_for_completion    = $false
} | ConvertTo-Json -Compress
