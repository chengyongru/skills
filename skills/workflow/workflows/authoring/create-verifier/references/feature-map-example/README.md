# Notes verification map

Example of a maintained user-facing verification map for a Notes application. Replace its names, commands, and controls with the target project's tested interface. Use the shape when authoring a real authorized workspace verifier; discover its actual commands/selectors instead of running these examples against an unrelated app. Read the index before a real verification run, then the matching feature recipe.

## Baseline preconditions

- Launch Notes at `http://127.0.0.1:4173` with a disposable data directory.
- Create a unique task-owned run root outside the plugin, with a separate data directory. A PowerShell setup for this fictional fixture is:

  ```powershell
  $RunRoot = Join-Path $env:TEMP ("notes-verify-" + [guid]::NewGuid().ToString("N"))
  $env:NOTES_DATA_DIR = Join-Path $RunRoot "data"
  ```

  Run the actual generated harness from its declared external run root. The feature examples' `artifacts/...` paths resolve beneath that root, never beneath the skill/package directory. Preserve evidence separately from disposable data.
- Seed notes titled `Quarterly plan` and `Grocery list`.
- For a real generated map, confirm its actual harness/CLI exists. `control-notes` and `notes` here are illustrative names, not dependencies to install automatically.
- Run `control-notes doctor` and require the expected URL, data directory, and build revision.
- Never drive an instance that was not started by this verification run.

## Driving conventions

- Start every recipe from the baseline state unless its preconditions say otherwise.
- Prefer ARIA roles and accessible names over CSS selectors or DOM position.
- In the real generated map, commands, quoted names, and flags are exact tested recipes.
- Run browser actions through `control-notes browser`.
- Run terminal actions through `control-notes cli -- <command>`.
- Restore seeded data after a mutation. Do not remove proof artifacts during cleanup.

## Proof and skip reporting

- Capture the user action and the resulting state, not only the final screen.
- UI proof includes an ARIA snapshot and a screenshot with the app identity visible.
- CLI proof includes the command, stdout, stderr, and exit code.
- Mutation proof includes a read-only second view of the stored value.
- Record the feature ID and entry point used with every artifact.
- Report an unreachable path with the attempted command and the unmet precondition.
- Do not report a skipped entry point as verified through a different path.

## Feature entry contract

Each feature file starts with an H1 title and one paragraph describing the user-visible behavior. It then uses exactly four H2 sections in this order.

1. `Sub-features` lists short IDs with one line for each behavior.
2. `How to get to it (user POV)` lists every user entry point.
3. `Driving it with <harness>` starts with `Preconditions:` and uses labeled bullets that pair each user action with an exact command and observable result.
4. `Gotchas` lists traps that can waste or invalidate a verification run.

Keep implementation details out of the map. Name only user paths, stable handles, required state, commands, and observable proof.

## Features

- [Create a note](create-note.md) covers browser and CLI creation, cancellation, persistence, and cleanup.
- [Search notes](search.md) covers toolbar, keyboard, and CLI search with matching, empty, and clear states.
