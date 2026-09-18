#Requires -Version 7.0
[CmdletBinding()]
param(
    [ValidateNotNullOrEmpty()]
    [string]$Cwd = (Get-Location).Path,
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Invoke-Herdr {
    param([string[]]$Arguments, [switch]$Text)

    $output = @(& herdr @Arguments 2>&1 | ForEach-Object { "$_" }) -join "`n"
    if ($LASTEXITCODE -ne 0) {
        throw "herdr $($Arguments -join ' ') failed: $output"
    }
    if ($Text) { return $output }
    $response = ConvertFrom-Json -InputObject $output -AsHashtable
    if (-not $response -or $response['error'] -or -not $response['result']) {
        throw "Herdr returned no successful result: $output"
    }
    return $response.result
}

function Test-WorktreePath {
    param([string]$Path)

    if (-not $Path -or -not [IO.Path]::IsPathFullyQualified($Path)) { return $false }
    $normalized = [IO.Path]::TrimEndingDirectorySeparator([IO.Path]::GetFullPath($Path))
    return [string]::Equals($normalized, $worktreeRoot, $pathComparison)
}

function Get-TargetPane {
    $pane = (Invoke-Herdr @('pane', 'get', $targetPaneId)).pane
    if ($pane.pane_id -ne $targetPaneId -or $pane.tab_id -ne $caller.tab_id) {
        throw "Target pane changed identity or tab: $targetPaneId"
    }
    return $pane
}

if ($env:HERDR_ENV -ne '1') {
    throw 'Run this helper inside a Herdr pane (HERDR_ENV=1).'
}

$rootOutput = @(& git -C $Cwd rev-parse --show-toplevel 2>&1 | ForEach-Object { "$_" })
if ($LASTEXITCODE -ne 0 -or $rootOutput.Count -ne 1) {
    throw "Cannot resolve the active Git worktree: $($rootOutput -join ' ')"
}
$worktreeRoot = [IO.Path]::TrimEndingDirectorySeparator([IO.Path]::GetFullPath($rootOutput[0]))
$pathComparison = if ($IsWindows) { [StringComparison]::OrdinalIgnoreCase } else { [StringComparison]::Ordinal }
$caller = (Invoke-Herdr @('pane', 'current', '--current')).pane
if (-not $caller.pane_id -or -not $caller.tab_id) { throw 'Herdr did not resolve the calling pane.' }

# Use the resolved ID: --current on neighbor/process-info can target UI focus instead.
$neighbor = (Invoke-Herdr @('pane', 'neighbor', '--pane', $caller.pane_id, '--direction', 'right')).neighbor
if ($neighbor.pane_id -ne $caller.pane_id -or $neighbor.layout.tab_id -ne $caller.tab_id) {
    throw 'Herdr returned a neighbor for a different caller or tab.'
}
$targetPaneId = $neighbor['neighbor_pane_id']
$action = if ($targetPaneId) { 'reuse' } else { 'create' }
$command = $null

if ($targetPaneId) {
    $rightIds = @($neighbor.layout.panes | ForEach-Object { $_.pane_id })
    if ($targetPaneId -eq $caller.pane_id -or $targetPaneId -notin $rightIds) {
        throw 'Herdr returned an invalid right-hand neighbor.'
    }
    $target = Get-TargetPane
    if (-not (Test-WorktreePath $target['cwd'])) {
        $processInfo = (Invoke-Herdr @('pane', 'process-info', '--pane', $targetPaneId)).process_info
        $foreground = @($processInfo['foreground_processes'] | Where-Object { $_ })
        if ($target['agent'] -or $processInfo.pane_id -ne $targetPaneId -or
            -not $processInfo['shell_pid'] -or $foreground.Count -ne 1 -or
            $foreground[0].pid -ne $processInfo.shell_pid) {
            throw "Right-hand pane $targetPaneId is occupied or its foreground shell is unknown."
        }
        $shellName = [IO.Path]::GetFileNameWithoutExtension($foreground[0].name).ToLowerInvariant()
        switch ($shellName) {
            { $_ -in 'pwsh', 'powershell' } {
                $command = "Set-Location -LiteralPath '" + $worktreeRoot.Replace("'", "''") + "'"
            }
            'cmd' {
                if ($worktreeRoot -match '[%!"\r\n]' -or $worktreeRoot.StartsWith('\\')) {
                    throw "The worktree path cannot be safely passed to cmd in $targetPaneId."
                }
                $command = 'cd /d "' + $worktreeRoot + '"'
            }
            { $_ -in 'bash', 'zsh', 'sh' } {
                if ($IsWindows) { throw "Windows path translation for $shellName in $targetPaneId is unsupported." }
                $command = "cd -- '" + $worktreeRoot.Replace("'", "'\''") + "'"
            }
            default { throw "Unsupported shell '$shellName' in right-hand pane $targetPaneId." }
        }
        $screen = Invoke-Herdr @('pane', 'read', $targetPaneId, '--source', 'recent-unwrapped', '--lines', '8') -Text
        $lastLine = @($screen -split '\r?\n' | Where-Object { $_.Trim() }) | Select-Object -Last 1
        if (-not $lastLine -or $lastLine -notmatch '[>❯➜$#%]\s*$') {
            throw "Right-hand pane $targetPaneId has no recognizable empty shell prompt."
        }
    }
}

if ($DryRun) {
    [ordered]@{
        status = 'dry-run'
        action = $action
        caller_pane_id = $caller.pane_id
        pane_id = $targetPaneId
        worktree = $worktreeRoot
        change_directory = [bool]$command
    } | ConvertTo-Json -Compress
    return
}

if ($action -eq 'create') {
    $created = (Invoke-Herdr @('pane', 'split', '--pane', $caller.pane_id, '--direction', 'right',
        '--cwd', $worktreeRoot, '--no-focus')).pane
    $targetPaneId = $created.pane_id
    if (-not $targetPaneId -or $targetPaneId -eq $caller.pane_id -or $created.tab_id -ne $caller.tab_id) {
        throw 'Herdr did not return a valid new pane in the calling tab.'
    }
} elseif ($command) {
    $null = Invoke-Herdr @('pane', 'run', $targetPaneId, $command) -Text
}

$timer = [Diagnostics.Stopwatch]::StartNew()
do {
    $target = Get-TargetPane
    if (Test-WorktreePath $target['cwd']) {
        [ordered]@{
            status = if ($action -eq 'create') { 'created' } else { 'reused' }
            caller_pane_id = $caller.pane_id
            pane_id = $targetPaneId
            worktree = $worktreeRoot
        } | ConvertTo-Json -Compress
        return
    }
    Start-Sleep -Milliseconds 200
} while ($timer.Elapsed.TotalSeconds -lt 5)

throw "Pane $targetPaneId did not report worktree '$worktreeRoot' within five seconds; current cwd: '$($target['cwd'])'."
