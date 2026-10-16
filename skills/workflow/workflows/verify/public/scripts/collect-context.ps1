param(
  [string]$Root = ".",
  [string]$OutDir = ""
)

$ErrorActionPreference = "Stop"

$resolvedRoot = (Resolve-Path -LiteralPath $Root).Path
if (-not $OutDir) {
  $OutDir = Join-Path $resolvedRoot (".verify-context-{0}" -f (Get-Date -Format "yyyyMMdd-HHmmss"))
}
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

function Save-Text {
  param([string]$Path, [string]$Text)
  $Text | Set-Content -LiteralPath $Path -Encoding UTF8
}

function Save-Command {
  param([string]$Name, [string[]]$Command)
  $path = Join-Path $OutDir $Name
  $start = Get-Date
  $output = New-Object System.Collections.Generic.List[string]
  $exitCode = 0
  try {
    $args = @()
    if ($Command.Length -gt 1) {
      $args = $Command[1..($Command.Length - 1)]
    }
    $result = & $Command[0] @args 2>&1
    if ($null -ne $result) {
      $result | ForEach-Object { $output.Add([string]$_) }
    }
    if ($null -ne $LASTEXITCODE) {
      $exitCode = $LASTEXITCODE
    }
  } catch {
    $exitCode = 1
    $output.Add($_.Exception.Message)
  }
  $durationMs = [int]((Get-Date) - $start).TotalMilliseconds
  $text = @(
    "command: $($Command -join ' ')",
    "exit_code: $exitCode",
    "duration_ms: $durationMs",
    "",
    ($output -join [Environment]::NewLine)
  ) -join [Environment]::NewLine
  Save-Text -Path $path -Text $text
}

Save-Command -Name "git-status.txt" -Command @("git", "-C", $resolvedRoot, "status", "--short", "--branch")
Save-Command -Name "git-log-head.txt" -Command @("git", "-C", $resolvedRoot, "log", "-1", "--oneline")
Save-Command -Name "git-diff-stat.txt" -Command @("git", "-C", $resolvedRoot, "diff", "--stat", "HEAD~1..HEAD")
Save-Command -Name "git-diff-name-status.txt" -Command @("git", "-C", $resolvedRoot, "diff", "--name-status", "HEAD~1..HEAD")
Save-Command -Name "git-diff-head.txt" -Command @("git", "-C", $resolvedRoot, "diff", "HEAD~1..HEAD")
Save-Command -Name "git-diff-working-tree.txt" -Command @("git", "-C", $resolvedRoot, "diff")
Save-Command -Name "git-diff-staged.txt" -Command @("git", "-C", $resolvedRoot, "diff", "--cached")

$patterns = @(
  "README*",
  "CLAUDE.md",
  "package.json",
  "Makefile",
  "docker-compose.yml",
  "docker-compose.yaml",
  "pyproject.toml",
  "Cargo.toml",
  "go.mod",
  "openapi.*",
  "swagger.*"
)

$manifestDir = Join-Path $OutDir "manifests"
New-Item -ItemType Directory -Force -Path $manifestDir | Out-Null

foreach ($pattern in $patterns) {
  Get-ChildItem -LiteralPath $resolvedRoot -Filter $pattern -File -ErrorAction SilentlyContinue |
    ForEach-Object {
      $destName = ($_.Name -replace '[\\/:*?"<>|]', "_")
      Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $manifestDir $destName) -Force
    }
}

Save-Text -Path (Join-Path $OutDir "summary.txt") -Text @"
root: $resolvedRoot
out_dir: $OutDir
created_at: $(Get-Date -Format o)

Read these files first:
- git-status.txt
- git-diff-name-status.txt
- git-diff-stat.txt
- manifests/

Use git-diff-head.txt, git-diff-working-tree.txt, and git-diff-staged.txt for detailed change analysis.
"@

Write-Output $OutDir
