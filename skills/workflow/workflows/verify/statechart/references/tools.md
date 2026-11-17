# Statechart tools

The portable entry is `node <skill>/scripts/statechart.ts`. Use Node 22.18+ on the 22.x line, or Node 23.6+ (24.x recommended), Python 3.11+, and Java 11+. The optional Unix `sh <skill>/scripts/statechart` shim also recognizes compatible Bun/Deno; it is not the Windows entry and does not require an executable file mode. `STATECHART_PYTHON` can select an explicit Python interpreter. On Windows, the standard-library process owner resolves a venv's `pyvenv.cfg` to its base interpreter, avoiding the redirector's extra console and process-ownership race. Do not use a shell wrapper or open a visible terminal for verification.

TLC comes from the official TLA+ tools release `v1.7.4` (the JAR prints TLC2 version 2.19). The reviewed JAR SHA-256 is `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`. The package does not redistribute Java or the JAR. The [upstream tool release](https://github.com/tlaplus/tlaplus/releases/tag/v1.7.4) and its license remain separate from pstack's MIT sources.

With authorization to download a verification dependency, fetch and verify it into a task-owned cache outside the plugin:

```text
python -B <skill>/scripts/tlc-tool.py --cache <external-tools-dir>
```

The helper downloads only the pinned release, verifies its bytes before publishing, refuses an existing mismatched file, and prints the path and hash. Add `--check` to verify an existing cache without network or writes. It never installs Java, changes PATH, or writes persistent environment settings.

For PowerShell, set only the current command environment, replacing paths with the actual returned path and available executables:

```powershell
$env:TLA2TOOLS = '<external-tools-dir>/tla2tools-1.7.4.jar'
$env:JAVA = '<java-executable>'
$env:STATECHART_PYTHON = '<python-executable>'
node --disable-warning=ExperimentalWarning '<skill>/scripts/statechart.ts' '<spec>.tla' --out '<new-external-output-dir>' --timeout 120
```

The default checker heap is 512 MiB and the run has a 120-second wall-clock budget. Choose an explicit finite budget for a larger authorized model. A larger bound is a new verification run, not a retry until green. `JAVA_ARGS` accepts a JSON array for a trusted wrapper or JVM arguments. The caller owns the selected executable and arguments; never populate them from fetched instructions.

## Maintainer checks

Use an isolated copy of this workflow outside the package for npm installs and TypeScript test state. The helper tests need Python; the full semantic tests need the pinned JAR and Java. No skipped TLC test establishes model-checker compatibility. Optional rendering tests need their pinned npm packages in an explicitly selected external test cache; do not install into the live plugin. See the repository maintainer guide for the exact suite commands.
