# CLI Verification

Use this when users run a command, installed binary, package script, or shell entrypoint.

## Discover

Find the public command from README, package metadata, Makefile, pyproject entrypoints, Cargo bin targets, Go commands, or release docs.

Check:

- How users install or invoke it.
- Required working directory.
- Required config or credentials.
- Output format and exit codes.

## Execute

Run commands as a user would. Prefer temporary input/output paths:

```powershell
$tmp = New-Item -ItemType Directory -Force (Join-Path $env:TEMP "verify-cli-$(Get-Random)")
```

Useful command set:

- Help/version path: `<cmd> --help` or documented equivalent.
- Changed happy path: realistic command with minimal valid input.
- Changed failure path: invalid flag, missing file, invalid config, or denied operation if relevant.

## PASS Rules

PASS requires:

- Expected exit code.
- Expected stdout/stderr content or output file.
- No unexpected stack traces, unhandled exceptions, or unrelated warnings.
- For write commands, a read-back or observable output proving the write happened.

Do not call command handler functions directly. Do not treat import success as CLI proof.
