param(
  [string]$OutDir = ".",
  [string]$Name = "",
  [Parameter(Mandatory = $true)]
  [string]$CommandLine
)

$ErrorActionPreference = "Stop"

if (-not $Name) {
  $Name = "command-{0}" -f (Get-Date -Format "yyyyMMdd-HHmmss")
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$safeName = $Name -replace '[\\/:*?"<>| ]', "_"
$stdoutPath = Join-Path $OutDir "$safeName.stdout.txt"
$stderrPath = Join-Path $OutDir "$safeName.stderr.txt"
$metaPath = Join-Path $OutDir "$safeName.meta.json"

$start = Get-Date
$exitCode = 0

try {
  $shell = "powershell"
  $found = Get-Command powershell -ErrorAction SilentlyContinue
  if ($found) {
    $shell = $found.Source
  }

  $process = Start-Process `
    -FilePath $shell `
    -ArgumentList @("-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", $CommandLine) `
    -RedirectStandardOutput $stdoutPath `
    -RedirectStandardError $stderrPath `
    -NoNewWindow `
    -Wait `
    -PassThru
  $exitCode = $process.ExitCode
} catch {
  $exitCode = 1
  $_.Exception.Message | Set-Content -LiteralPath $stderrPath -Encoding UTF8
  if (-not (Test-Path -LiteralPath $stdoutPath)) {
    "" | Set-Content -LiteralPath $stdoutPath -Encoding UTF8
  }
}

$end = Get-Date
$meta = [ordered]@{
  command_line = $CommandLine
  working_directory = (Get-Location).Path
  started_at = $start.ToString("o")
  ended_at = $end.ToString("o")
  duration_ms = [int]($end - $start).TotalMilliseconds
  exit_code = $exitCode
  stdout = $stdoutPath
  stderr = $stderrPath
}

$meta | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $metaPath -Encoding UTF8

Write-Output "exit_code=$exitCode"
Write-Output "stdout=$stdoutPath"
Write-Output "stderr=$stderrPath"
Write-Output "meta=$metaPath"

exit $exitCode
