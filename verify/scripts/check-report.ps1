param(
  [Parameter(Mandatory = $true)]
  [string]$ReportPath
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $ReportPath)) {
  throw "Report not found: $ReportPath"
}

$text = Get-Content -LiteralPath $ReportPath -Raw
$errors = New-Object System.Collections.Generic.List[string]
$warnings = New-Object System.Collections.Generic.List[string]

foreach ($section in @("Verification Report", "Evidence", "Conclusion")) {
  if ($text -notmatch [regex]::Escape($section)) {
    $errors.Add("Missing section or marker: $section")
  }
}

if ($text -match "\bPASS\b" -and $text -notmatch "(?i)evidence") {
  $errors.Add("PASS appears without an evidence section or marker.")
}

if ($text -match "\bPASS\b" -and $text -notmatch "(?i)pass rule|pass_rule") {
  $warnings.Add("PASS appears without an explicit pass rule marker.")
}

$hedges = @("should work", "probably", "looks fine", "seems fine", "likely works")
foreach ($hedge in $hedges) {
  if ($text.ToLowerInvariant().Contains($hedge)) {
    $warnings.Add("Hedging phrase found: $hedge")
  }
}

if ($errors.Count -gt 0) {
  Write-Output "FAIL"
  $errors | ForEach-Object { Write-Output "ERROR: $_" }
  $warnings | ForEach-Object { Write-Output "WARN: $_" }
  exit 1
}

Write-Output "PASS"
$warnings | ForEach-Object { Write-Output "WARN: $_" }
